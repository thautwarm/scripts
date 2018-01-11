import numpy as np
from pipe_fn import infix, and_then
from linq.standard.general import Map

def gaussian_noise(img):
    """
    高斯噪声
    仅接受灰度图
    """
    normal = np.random.normal(0, 1/255, size=(img.shape[:2]))
    return img + normal


salt = 0
peper = 1
other = 2

def salt_and_pepper(img, prob = 0.01, salt_prob=0.5):
    """
    适用于单色道图或者灰度图。根据prob概率返回一个椒盐化图。椒化和盐化概率为salt_prob。
    """
    
    rnds = np.random.random(img.shape[:2])
    
    salt_types = np.random.random(img.shape[:2]) # 是255还是0
    
    salt_peper_indices = np.vectorize(
                lambda rnd, salt_type: ((
                        salt if salt_type>0.5 else 
                        peper) if prob > rnd else other), 
                        signature='(),()->()')(
                                    rnds, salt_types).reshape(img.shape[:2])
    
    img = img.copy()
    
    if img.ndim is 3:
        if img.shape[2] is 3:
            img[salt_peper_indices == salt] = np.array([255, 255, 255])
            img[salt_peper_indices == peper] = np.array([0, 0, 0])
        else:
            img[salt_peper_indices == salt] = np.array([255])
            img[salt_peper_indices == peper] = np.array([0])
    else:
        img[salt_peper_indices == salt] = 255
        img[salt_peper_indices == peper] = 0
    
    return img


def poisson_noise(img):
    """
    泊松噪声
    仅接受灰度图
    """
    poisson_noise_dist = np.random.poisson(1/5, img.shape[:2]).astype(float)
    return poisson_noise_dist + img