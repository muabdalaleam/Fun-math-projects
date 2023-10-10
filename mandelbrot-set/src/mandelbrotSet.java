import processing.core.PApplet;

public class mandelbrotSet extends PApplet {

    public void settings() {
        size(1000, 750);
        noLoop();
    }

    public void draw() {
        loadPixels();

        // =============== Constants ===============
        float xmin = (float) -2;
        float xmax = (float) 1.5;
        float ymin = (float) -1.3;
        float ymax = (float) 1.3;
        
        int maxIters = 500;

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                // =========================================
                
                // =============== Math Logic ===============
                float a = map(x, 0, width, xmin, xmax);
                float b = map(y, 0, height, ymin, ymax);
                float za = a;
                float zb = b;
                int i;
                
                for (i = 0; i < maxIters; i++) {
                    float a_temp = a * a - b * b;
                    float b_temp = 2 * a * b;
                    
                    a = a_temp + za;
                    b = b_temp + zb;
                    
                    if (abs(a + b) > 16) {
                    break;
                    }
                }
                // =========================================
                
                //  =============== Coloring the fractal ===============
                float brightness = map(i, 0, maxIters, 0, 1);
                
                int R;
                int G;
                int B;
                
                if (i == maxIters) {
                    brightness = 0;
                    
                    R = (int) map(brightness, 0, 1, 0, 255);
                    G = (int) map(brightness, 0, 1, 0, 255);
                    B = (int) map(brightness, 0, 1, 0, 255);
                }
                
                else {
                    brightness = (float) (log(brightness) / 1.4);
                    
                    R = (int) map(brightness, 0, 1, 100, 255);
                    G = (int) map(brightness, 0, 1, 200, 255);
                    B = (int) map(brightness, 0, 1, 100, 255);
                }
                
                int pix = x + y * width;
                
                pixels[pix] = color(R, G, B);
                // ======================================================
            }
        }
        
        updatePixels();
        save("madelbrot.png");
    }

    public static void main(String[] args) {
        PApplet.main("mandelbrotSet");
    }
}