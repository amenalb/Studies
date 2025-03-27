package com.example.wypozyczalna_samochodow;

import javafx.application.Application;
import javafx.stage.Stage;

public class HelloApplication extends Application {

    @Override
    public void start(Stage primaryStage) {
        CarShowroomGUI carShowroomApp = new CarShowroomGUI();
        try {
            carShowroomApp.start(primaryStage);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
