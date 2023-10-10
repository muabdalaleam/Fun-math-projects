import processing.core.PApplet;;

public class fractalTree extends PApplet {

    float deg;
    int GREEN = color(100, 194, 89);
    int BROWN = color(79, 74, 65);

    public void settings() {
      size(850, 600);
    }


    public void draw() {
      background(color(173, 245, 255));
      frameRate(30);
    
      float line_length  = height * (float) 0.3;
      float middle_point = width / 2;
    
      deg = (mouseX / (float) width) * 90f;
    
      stroke(BROWN);
      strokeWeight(5);
      translate(middle_point, height);
      line(0, 0, 0, -line_length);
      translate(0, -line_length);
    
      drawFractal(line_length);
    }
    
    void drawFractal(float len) {
      float shrinking_factor = (float) 0.7;
      float theta0 = radians(deg);
      float theta1 = -radians((90-deg));
    
      len *= shrinking_factor;
    
      if (len < 30) {
        stroke(GREEN);
        strokeWeight(3);
      } else {
        stroke(BROWN);
        strokeWeight(5);
      }
    
      if (len > 3) {
        pushMatrix();
        rotate(theta0);
        line(0, 0, 0, -len);
        translate(0, -len);
        drawFractal(len);
        popMatrix();
    
        if (len < 30) {
          stroke(GREEN);
          strokeWeight(3);
        } else {
          stroke(BROWN);
          strokeWeight(5);
        }
    
        pushMatrix();
        rotate(theta1);
        line(0, 0, 0, -len);
        translate(0, -len);
        drawFractal(len);
        popMatrix();
      }
    }
    

    public static void main(String[] args) {
        PApplet.main("fractalTree");
    }
}