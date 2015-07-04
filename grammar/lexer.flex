
import java_cup.runtime.*;

%%

%public
%class Lexer
%unicode
%cup
%line
%column

%{
    StringBuffer string = new StringBuffer();

    private Symbol symbol(int type) {
        return new Symbol(type, yyline, yycolumn);
    }
    private Symbol symbol(int type, Object value) {
        return new Symbol(type, yyline, yycolumn, value);
    }

%}

LineTerminator = \r|\n|\r\n
WhiteSpace     = {LineTerminator} | [ \t\f]

BitLiteral = 0 | 1

%%

"&" { return symbol(sym.AND); }
"|" { return symbol(sym.OR); }
"~" { return symbol(sym.NOT); }
"(" { return symbol(sym.LPAREN); }
")" { return symbol(sym.RPAREN); }

{BitLiteral} {
    String lexeme = yytext();
    int x = 2;
    try {
        x = Integer.parseInt(lexeme);
    }
    catch(NumberFormatException nfe) {
        assert false : "Not a number: " + lexeme;
    }
    if (x == 1) return symbol(sym.TRUE);
    else if (x == 0) return symbol(sym.FALSE);
    else {
        assert false;
        return null;
    }
}


{WhiteSpace} { /* ignore */ }

.|\n { throw new Error("Illegal character "+ yytext()); }
