package com.example.wypozyczalna_samochodow;

import com.example.wypozyczalna_samochodow.CarShowroomContainer;
import com.example.wypozyczalna_samochodow.Vehicle;
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.event.ActionEvent;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class CarShowroomGUI extends Application {

    private CarShowroomContainer container;
    private ComboBox<String> showroomComboBox;
    private TextField searchField; // Pole tekstowe do wyszukiwania
    private ListView<Vehicle> vehicleListView;
    private TableView<Vehicle> vehicleTableView;

    @Override
    public void start(Stage primaryStage) {
        // Inicjalizacja kontenera i dodanie próbnych pojazdów
        container = new CarShowroomContainer();
        container.addCenter("Showroom1", 2);
        System.out.println("Number of showrooms: " + container.getShowrooms().size());
        container.addCenter("Showroom2", 5);
        container.addCenter("Showroom3", 4);
        System.out.println("Number of showrooms: " + container.getShowrooms().size());
        addSampleVehicles();

        // Tworzenie UI
        showroomComboBox = new ComboBox<>();
        showroomComboBox.setItems(FXCollections.observableArrayList("Showroom1", "Showroom2", "Showroom3", "Dowolny"));
        showroomComboBox.setValue("Dowolny");

        searchField = new TextField();
        searchField.setPromptText("Search by name");

        vehicleListView = new ListView<>();
        vehicleTableView = new TableView<>();

        Button searchButton = new Button("Search");
        searchButton.setOnAction(event -> searchVehicleByBrand());

        Button deleteButton = new Button("Buy Vehicle");
        deleteButton.setOnAction(event -> deleteVehicle());

        // Układ UI
        VBox root = new VBox(10);
        root.setPadding(new Insets(10));
        root.getChildren().addAll(showroomComboBox, new HBox(searchField, searchButton, deleteButton), vehicleListView, vehicleTableView);

        // Tworzenie sceny i ustawienie UI
        Scene scene = new Scene(root, 600, 400);
        primaryStage.setScene(scene);
        primaryStage.setTitle("Car Showroom");
        primaryStage.show();

        // Inicjalizacja komponentów UI
        initializeUIComponents();

        // Wybierz domyślną opcję "Dowolny" i wyświetl wszystkie pojazdy
        showroomComboBox.getSelectionModel().select("Dowolny");
        showroomComboBox.fireEvent(new ActionEvent());
    }

    private void initializeUIComponents() {
        showroomComboBox.setOnAction(e -> {
            String selectedShowroom = showroomComboBox.getValue();
            if (selectedShowroom.equals("Dowolny")) {
                showAllVehicles();
            } else {
                showVehiclesInShowroom(selectedShowroom);
            }
        });
        //listView
        vehicleListView.setCellFactory(param -> new ListCell<Vehicle>() {
            @Override
            protected void updateItem(Vehicle item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || item == null) {
                    setText(null);
                    setTooltip(null);
                } else {
                    setText(item.getBrand() + " " + item.getModel());
                    Tooltip tooltip = new Tooltip("Mileage: " + item.getMileage() + "\nEngine: " + item.getEngineCapacity());
                    setTooltip(tooltip);
                }
            }
        });

        TableColumn<Vehicle, String> brandColumn = new TableColumn<>("Brand");
        brandColumn.setCellValueFactory(new PropertyValueFactory<>("brand"));
        TableColumn<Vehicle, String> modelColumn = new TableColumn<>("Model");
        modelColumn.setCellValueFactory(new PropertyValueFactory<>("model"));
        TableColumn<Vehicle, ItemCondition> conditionColumn = new TableColumn<>("Condition");
        conditionColumn.setCellValueFactory(new PropertyValueFactory<>("condition"));
        TableColumn<Vehicle, Double> priceColumn = new TableColumn<>("Price");
        priceColumn.setCellValueFactory(new PropertyValueFactory<>("price"));
        TableColumn<Vehicle, Integer> yearColumn = new TableColumn<>("Year");
        yearColumn.setCellValueFactory(new PropertyValueFactory<>("productionYear"));
        TableColumn<Vehicle, Double> engineColumn = new TableColumn<>("Engine Capacity");
        engineColumn.setCellValueFactory(new PropertyValueFactory<>("engineCapacity"));

        vehicleTableView.getColumns().addAll(brandColumn, modelColumn, conditionColumn, priceColumn, yearColumn, engineColumn);

        vehicleTableView.setRowFactory(param -> new TableRow<Vehicle>() {
            @Override
            protected void updateItem(Vehicle item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || item == null) {
                    setTooltip(null);
                } else {
                    Tooltip tooltip = new Tooltip("Mileage: " + item.getMileage() + "\nEngine: " + item.getEngineCapacity());
                    setTooltip(tooltip);
                }
            }
        });
    }

    private void deleteVehicle() {
        Vehicle selectedVehicle = vehicleTableView.getSelectionModel().getSelectedItem();
        if (selectedVehicle != null) {
            String selectedShowroom = showroomComboBox.getValue();
            CarShowroom showroom = container.getShowroom(selectedShowroom);
            if (showroom != null) {
                showroom.removeVehicle(selectedVehicle); // Usunięcie pojazdu z salonu
                // Odświeżenie widoku
                showroomComboBox.fireEvent(new ActionEvent());
                // Odśwież widok tabeli
                vehicleTableView.refresh();
            }
        } else {
            // Wyświetlenie ostrzeżenia, jeśli nie wybrano żadnego pojazdu
            Alert alert = new Alert(Alert.AlertType.WARNING);
            alert.setTitle("Warning");
            alert.setHeaderText(null);
            alert.setContentText("Please select a vehicle to buy!");
            alert.showAndWait();
        }
    }


    private void searchVehicleByBrand() {
        String searchText = searchField.getText().trim().toLowerCase();
        if (!searchText.isEmpty()) {

            List<Vehicle> filteredList = new ArrayList<>();
            System.out.println("Number of showrooms: " + container.getShowrooms().size());

            for (Map.Entry<String, CarShowroom> entry : container.getShowrooms().entrySet()) {

                CarShowroom showroom = entry.getValue();
                if (showroom != null) {
                    for (Vehicle vehicle : showroom.getInventory().keySet()) {
                        String brand = vehicle.getBrand().toLowerCase();
                        if (brand.contains(searchText)) {
                            filteredList.add(vehicle);
                        }
                    }
                }
            }

            vehicleListView.getItems().clear();
            vehicleTableView.getItems().clear();

            vehicleListView.getItems().addAll(filteredList);
            vehicleTableView.getItems().addAll(filteredList);
        }
    }


    private void showAllVehicles() {
        vehicleListView.getItems().clear();
        vehicleTableView.getItems().clear();
        for (Map.Entry<String, CarShowroom> entry : container.getShowrooms().entrySet()) {
            CarShowroom showroom = entry.getValue();
            if (showroom != null) {
                for (Vehicle vehicle : showroom.getInventory().keySet()) {
                    vehicleListView.getItems().add(vehicle);
                    vehicleTableView.getItems().add(vehicle);
                }
            }
        }
    }

    private void showVehiclesInShowroom(String showroomName) {
        vehicleListView.getItems().clear();
        vehicleTableView.getItems().clear();
        CarShowroom showroom = container.getShowroom(showroomName);
        if (showroom != null) {
            for (Vehicle vehicle : showroom.getInventory().keySet()) {
                vehicleListView.getItems().add(vehicle);
                vehicleTableView.getItems().add(vehicle);
            }
        }
    }

    private void addSampleVehicles() {
        container.getShowroom("Showroom1").addVehicle(new Vehicle("Toyota", "Corolla", ItemCondition.NEW, 25000.0, 2023, 10000.0, 1.8));
        container.getShowroom("Showroom1").addVehicle(new Vehicle("Ford", "Mustang", ItemCondition.USED, 35000.0, 2019, 5000.0, 5));
        container.getShowroom("Showroom2").addVehicle(new Vehicle("BMW", "X5", ItemCondition.NEW, 60000.0, 2022, 2000.0, 3.0));
        container.getShowroom("Showroom3").addVehicle(new Vehicle("Honda", "Civic", ItemCondition.USED, 20000.0, 2020, 8000.0, 1.6));
        container.getShowroom("Showroom3").addVehicle(new Vehicle("Mercedes", "C-Class", ItemCondition.NEW, 55000.0, 2023, 1500.0, 2.0));
        container.getShowroom("Showroom3").addVehicle(new Vehicle("Audi", "A4", ItemCondition.NEW, 50000.0, 2023, 2000.0, 2.0));
    }

    public static void main(String[] args) {
        launch(args);
    }
}
