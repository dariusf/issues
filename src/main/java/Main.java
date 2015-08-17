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

    private static void test(String s) {
        System.out.println("hello");
    }

    public static void main(String[] args) {
        int useless = 1;
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
