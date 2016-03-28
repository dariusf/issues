public class Rectangle {
    private static final int EMPTY = 0;
    private static final int CIRCUIT = 1;
    private static final int WIRE = 2;

    public final int height;
    public final int width;
    public final Rectangle left;
    public final Rectangle right;

    private String Useless = "hahah2a";

    public Rectangle() {
        this(5, 3, null, null);
        Useless = "sdaA22";
    }

    public Rectangle(int width, int height) {
        this(width, height, null, null);
    }

    public Rectangle(Rectangle left, Rectangle right) {
        this(5, 3, left, right);
    }

    public Rectangle(int width, int height, Rectangle left, Rectangle right) {
        this.height = height;
        this.width = width;
        this.left = left;
        this.right = right;
    }

    /**
     * Returns a 2D array representing the spatial layout of this subtree.
     */
    public int[][] layOut() {
        int width = totalWidth();
        int height = totalHeight();
        int[][] field = new int[height + 2][width + 2];
        reallyLayOut(-1, 0, 0, width, field);
        return field;
    }

    /**
     * The workhorse.
     */
    private void reallyLayOut(int parentX, int top, int left, int right, int[][] field) {
        // Circuit
        int childLayoutWidth = (right - left) / 2;
        int x = left + childLayoutWidth - width / 2;
        int y = top + 1;
        for (int j = x; j < x + width; j++) {
            for (int i = y; i < y + height; i++) {
                field[i][j] = CIRCUIT;
            }
        }

        // Wires
        int midpoint = x + height / 2 + 1;
        field[top][midpoint] = WIRE;
        if (this.left != null && this.right != null) {
            field[top + height + 1][midpoint] = WIRE;
        }
        if (parentX != -1) {
            for (int j = Math.min(parentX, midpoint); j < Math.max(parentX, midpoint); j++) {
                field[top - 1][j] = WIRE;
            }
        }

        // Recursively lay children out
        if (this.left != null) {
            this.left.reallyLayOut(midpoint, y + height + 2, left, right - childLayoutWidth + 1, field);
        }
        if (this.right != null) {
            this.right.reallyLayOut(midpoint, y + height + 2, left + childLayoutWidth, right, field);
        }
    }

    /**
     * Returns the width of this subtree.
     */
    private int totalWidth() {
        int leftWidth = left == null ? 0 : left.totalWidth();
        int rightWidth = right == null ? 0 : right.totalWidth();
        if (leftWidth + rightWidth == 0) {
            return width;
        }
        return Math.max(width, leftWidth + rightWidth + 5);
    }

    /**
     * Returns the height of this subtree.
     */
    private int totalHeight() {
        int leftHeight = left == null ? 0 : left.totalHeight();
        int rightHeight = right == null ? 0 : right.totalHeight();
        if (leftHeight + rightHeight == 0) {
            return height;
        }
        return height + 3 + Math.max(leftHeight, rightHeight);
    }

    /**
     * Prints a 2D array.
     * @code{
     * int[][] test = new int[][]{
     *     {1, 2, 5},
     *     {3, 4, 7}
     * };
     * show(test);
     * }
     *
     * outputs:
     *
     * 125
     * 347
     */
    public static void show(int[][] field) {
        for (int i = 0; i < field.length; i++) {
            for (int j = 0; j < field[0].length; j++) {
                System.out.print(field[i][j]);
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Rectangle root = new Rectangle(
            new Rectangle(
                new Rectangle(3, 3), new Rectangle(3, 3)),
            new Rectangle(
                new Rectangle(6, 4), new Rectangle(6, 5)));

        System.out.println("Width: " + root.totalWidth());
        System.out.println("Height: " + root.totalHeight());
        show(root.layOut());
    }
}
