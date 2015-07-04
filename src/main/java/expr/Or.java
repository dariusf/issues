package expr;

public class Or implements Expr {
    final Expr left;
    public final Expr right;

    public Or(Expr left, Expr right) {
        this.left = left;
        this.right = right;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        And and = (And) o;

        if (left != null ? !left.equals(and.left) : and.left != null) return false;
        if (right != null ? !right.equals(and.right) : and.right != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        int result = left != null ? left.hashCode() : 0;
        result = 31 * result + (right != null ? right.hashCode() : 0);
        return result;
    }

    @Override
    public String toString() {
        return String.format("(%s | %s)", left, right);
    }
}
