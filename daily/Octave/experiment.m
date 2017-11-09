
Size = 500;
F    = @(x,y)(x+y+1);
iters= 5;
rate = 0.5;

bases = rand(Size,1)*2*pi;
X     = cos(bases);
Y     = sin(bases);
Datas  = [X Y];
R      = 2 .* rand(Size, 1);
R      = [R R];
Datas  = Datas .* R;
X      = Datas(:, 1);
Y      = Datas(:, 2);


Targets= F(X, Y);
SmallThan0 = Targets<0;
Targets( SmallThan0)  = -1;
Targets(~SmallThan0) =  1;

Weight = rand(1, 2);
Bias   = rand();

for iter=1:iters;
	for i=1:Size;
		data   = Datas(i, :);
		target = Targets(i);
		output = Weight * data' + Bias;
		if output*target <= 0 ;	
			Weight = Weight + (rate.*target).*data;
			Bias   = Bias   + rate.*target;
		end
	end
end

y_pred = sign(Bias .+  Datas * Weight');
y_true = Targets;
disp([y_pred y_true])

subplot(211)
scatter(Datas(:, 1), Datas(:, 2), 5*ones(Size,1), y_true ,'filled' )
subplot(212)
scatter(Datas(:, 1), Datas(:, 2), 5*ones(Size,1), y_pred ,'filled'  )
input('press ENTER and exit.');






