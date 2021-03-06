import java.io.StringReader;
import java.util.Optional;

import expr.Expr;
import java.util.*;

public class Main {

    public static int FAKE_CONSTANT = 1;

    public static class Proxy {
        Date date;
        public Proxy(Date date) {
            FAKE_CONSTANT = 2;
            this.date = date;
        }
    }

    private static void test(String s) {
        System.out.println("hello");

    }

    private int useless = 1;
    private int moreuseless = 0;
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
