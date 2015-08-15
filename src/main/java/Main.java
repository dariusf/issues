import java.io.StringReader;
import java.util.Optional;

import expr.Expr;
import java.util.*;

public class Main {

    public static int FAKE_CONSTANT = 1;

    public static class Proxy {
        Date date;
        public Proxy(Date date) {
            this.date = date;
        }
    }

    private static Optional<Expr> parse(String s) {
        Expr result;
        try {
            parser p = new parser(new Lexer(new StringReader(s + "\n")));
            result = (Expr) p.parse().value;
        } catch (Throwable e) {
            return Optional.empty();
        }
        return Optional.of(result);
    }

    private static void test(String s) {
        System.out.printf("%s => %s\n", s, parse(s));
    }

    public static void main(String[] args) {
        test("1");
        test("0");
        test("1 & 0");
        test("~1 | 0");
        test("1 | 0 & 1");
        test("(1 | 0) & 1");

        test("~1");
        test("~(1)");
        test("~(1 | 0)");
        test("~(1 | 0) & 1");
        test("2");
    }
}
