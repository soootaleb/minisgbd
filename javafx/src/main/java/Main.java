import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
 
public class Main extends Application {
    public static void main(String[] args) {
        launch(args);
    }
    
    @Override
    public void start(Stage stage) {

        stage.setTitle("JavaFX");

        Button btn = new Button();
        btn.setText("Fetch from API");

        btn.setOnAction(new EventHandler<ActionEvent>() {
 
            @Override
            public void handle(ActionEvent event) {
                System.out.println("Hello Wuorld!");
            }
        });
        
        StackPane root = new StackPane();
        root.getChildren().add(btn);

        stage.setScene(new Scene(root, 600, 500));
        stage.show();
    }
}