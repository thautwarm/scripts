

object parserc {
  case class Token[T](lineno: Int, colno: Int, value: T, name: String = "", filename: String = "")

  type Parsing[E, T] = Option[(T, List[Token[E]])]

  case class Parser[E, T](f: List[Token[E]] => Parsing[E, T]) {

    def apply(tokens: List[Token[E]]) = f(tokens)
    def +[G](g: Parser[E, G]): Parser[E, (T, G)] = {

      Parser {
        tokens =>
          f(tokens) match {
            case None => None
            case Some((a, tokens)) =>
              g(tokens) match {
                case None              => None
                case Some((b, tokens)) => Some((a, b), tokens)
              }
          }
      }
    }

    def |(g: Parser[E, T]) = {
      Parser {
        (tokens: List[Token[E]]) =>
          f(tokens) match {
            case None => g(tokens)
            case res  => res
          }
      }
    }

    def ? = {
      Parser {
        (tokens: List[Token[E]]) =>
          f(tokens) match {
            case None              => Some((None, tokens))
            case Some((v, tokens)) => Some((Some(v), tokens))
          }
      }
    }

    def *(least: Int, most: Int) = {
      Parser {
        def app(res: List[T])(tokens: List[Token[E]]): Parsing[E, List[T]] =
          f(tokens) match {
            case None => {
              if (res.length >= least)
                Some((res.reverse, tokens))
              else
                None
            }
            case Some((v, tokens)) => {
              val lst = v :: res
              if (most equals (lst.length))
                Some((lst.reverse, tokens))
              else
                app(lst)(tokens)
            }
          }
        app(List())
      }
    }

    def ->[G](rewrite: T => G) = {
      Parser {
        (tokens: List[Token[E]]) =>
          f(tokens) match {
            case None              => None
            case Some((v, tokens)) => Some((rewrite(v), tokens))
          }
      }
    }
    
   def >>[V](p: Parser[E, V]) = (this + p) -> ({case (a, b) => b})
   def <<[V](p: Parser[E, V]) = (this + p) -> ({case (a, b) => a})
   
  }
   
  
  def lex_char(text: String) = text.toCharArray().map(x => Token(0, 0, x))

  def match_ch(ch: Char) =
    Parser {
      (tokens: List[Token[Char]]) =>
        tokens match {
          case (head @ Token(_, _, ch_, _, _)) :: tail if ch_ equals ch => Some((head, tail))
          case _                                      => None
        }
    }
  
  def match_ch_when(f: Char => Boolean) =
    Parser {
      (tokens: List[Token[Char]]) =>
        tokens match {
          case (head @ Token(_, _, ch, _, _)) :: tail if f(ch) => Some((head, tail))
          case _                                      => None
        }
    }    
}