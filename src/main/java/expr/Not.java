package expr;

public class Not implements Expr {
    public final Expr e;

    public Not(Expr e) {
        this.e = e;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Not not = (Not) o;

        if (e != null ? !e.equals(not.e) : not.e != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        return e != null ? e.hashCode() : 0;
    }

    @Override
    public String toString() {
        return String.format("(~%s)", e);
    }
}
