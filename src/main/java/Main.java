import java.io.StringReader;
import java.util.Optional;

import expr.Expr;
import java.util.*;

public class Main {

    public static int FAKE_CONSTANT = 1;

    public static class Proxy {
        Date date;
        Date date2;
        public Proxy(Date date) {
            this.date = date;
            this.date2 = date;
        }
    }

    private static void test(String s) {
        System.out.println("hello");
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
