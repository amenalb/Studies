package com.example.wypozyczalna_samochodow;

import com.example.wypozyczalna_samochodow.Vehicle;

import java.util.*;

public class CarShowroom {
    private String showroomName;
    private int maxCapacity;
    private int capacity=0;
    Map<Vehicle, Integer> inventory; //ilosc pojazdow
    public CarShowroom(String showroomName, int maxCapacity, Map<String, Integer> inventory) {
        this.showroomName = showroomName;
        this.maxCapacity = maxCapacity;
        this.inventory = new HashMap<>();
    }

    public CarShowroom(String showroomName, int maxCapacity) {
        this.showroomName = showroomName;
        this.maxCapacity = maxCapacity;
        this.inventory = new HashMap<>();
    }


    public void addVehicle(Vehicle vehicle){
        if (capacity >= maxCapacity) {
            System.err.println("Cannot add vehicle. Showroom capacity exceeded.");
            return;
        }

        Integer currentQuantity = inventory.get(vehicle);
        if (currentQuantity != null) {
            inventory.put(vehicle, currentQuantity + 1);
        } else {
            inventory.put(vehicle, 1);
        }
        capacity++;
        System.out.println("Added");
    }
    public void getProduct(Vehicle vehicle) {
        Integer currentQuantity = inventory.getOrDefault(vehicle, 0);
        if (currentQuantity > 0) {
            if (currentQuantity == 1) {
                inventory.remove(vehicle);
                System.out.println("Removed " + vehicle.brand + " " + vehicle.model + " from inventory.");
            } else {
                inventory.put(vehicle, currentQuantity - 1); // Zmniejsz ilość pojazdu o jeden
                System.out.println("Decreased quantity of " + vehicle.brand + " " + vehicle.model + " in inventory.");
            }
            capacity--;
        } else {
            System.err.println("Vehicle not found in inventory.");
        }
    }
    public void removeProduct(Vehicle vehicle){
        String vehicleName = vehicle.brand+vehicle.model;
        if (inventory.containsKey(vehicleName)) {
            inventory.remove(vehicleName);
            System.out.println("Removed " + vehicleName + " from inventory.");
            capacity--;
        }
        else{
            System.err.println("Vehicle not found in inventory.");
        }
    }
    public Vehicle search(String name) {
        List<Vehicle> sortedVehicles = new ArrayList<>(inventory.keySet());
        sortedVehicles.sort(Comparator.comparing(Vehicle::getBrand));
        for (Vehicle vehicle : sortedVehicles) {
            if (vehicle.getBrand().equalsIgnoreCase(name) || vehicle.getModel().equalsIgnoreCase(name)) {
                System.out.println("Vehicle was found");
                return vehicle;
            }
        }
        System.out.println("Vehicle wasn't found");
        return null;
    }
    public List<Vehicle> searchPartial(String partialName) {
        List<Vehicle> matchingVehicles = new ArrayList<>();
        for (Vehicle vehicle : inventory.keySet()) {
            if (vehicle.getBrand().toLowerCase().contains(partialName.toLowerCase()) ||
                    vehicle.getModel().toLowerCase().contains(partialName.toLowerCase())) {
                System.out.println("Vehicle was found");
                matchingVehicles.add(vehicle);
            }
        }
        return matchingVehicles;
    }
    public int countByCondition(ItemCondition condition) {
        int count = 0;
        for (Map.Entry<Vehicle, Integer> entry : inventory.entrySet()) {
            if (entry.getKey().getCondition() == condition) {
                count += entry.getValue();
            }
        }
        System.out.println("count: "+count);
        return count;
    }
    public void summary() {
        System.out.println("Summary of vehicles in showroom ");
        for (Map.Entry<Vehicle, Integer> entry : inventory.entrySet()) {
            Vehicle vehicle = entry.getKey();
            int quantity = entry.getValue();
            System.out.println("Vehicle: " + vehicle.getBrand() + " " + vehicle.getModel() + ", Quantity: " + quantity);
        }
        System.out.println("Total amount of Vehicles: " + capacity + " / " + maxCapacity);
    }
    public List<Vehicle> sortByName() {
        //Sortuje używając komparatora, który porównuje pojazdy najpierw według (getBrand()), a następnie według (getModel()).
        List<Vehicle> sortedList = new ArrayList<>(inventory.keySet());
        Collections.sort(sortedList, Comparator.comparing(Vehicle::getBrand).thenComparing(Vehicle::getModel));
        System.out.println("Sorted List by Name:");
        for (Vehicle vehicle : sortedList) {
            System.out.println(vehicle.getBrand() + " " + vehicle.getModel());

        }
        return sortedList;
    }
    public List<Vehicle> sortByAmount() {
        List<Vehicle> vehiclesList = new ArrayList<>(inventory.keySet());
        // Sortowanie listy pojazdów według ilości malejąco
        Collections.sort(vehiclesList, Comparator.comparingInt(inventory::get).reversed());
        System.out.println("Sorted List by Amount:");
        for (Vehicle vehicle : vehiclesList) {
            System.out.println(vehicle.getBrand() + " " + vehicle.getModel());

        }
        return vehiclesList;
    }
    public Vehicle max() {
        if (inventory.isEmpty()) {
            return null;
        }


        // Używamy Collections.max() do znalezienia maksymalnej ilości pojazdu w mapie
        int maxQuantity = Collections.max(inventory.values());

        for (Map.Entry<Vehicle, Integer> entry : inventory.entrySet()) {
            if (entry.getValue() == maxQuantity) {
                System.out.println("Vehicle was found");
                return entry.getKey();
            }
        }
        return null; // Jeśli nie znaleziono pojazdu
    }

    public int getCapacity() {
        return this.capacity;
    }

    public int getMaxCapacity() {
        return maxCapacity;
    }

    public String getShowroomName() {
        return showroomName;
    }

    public List<Vehicle> getVehicles() {
        return List.of();
    }
    public Map<Vehicle, Integer> getInventory() {
        return inventory;
    }
    public void removeVehicle(Vehicle vehicle) {
        inventory.remove(vehicle); // Usunięcie pojazdu z magazynu
    }





}
