package com.example.wypozyczalna_samochodow;

import javafx.beans.value.ObservableValue;

public class Vehicle implements java.lang.Comparable<Vehicle> {
    String brand;
    String model;
    ItemCondition condition;
    double price;
    int productionYear;
    double mileage;
    double engineCapacity;

    public Vehicle(String brand, String model, ItemCondition condition, double price, int productionYear, double mileage, double engineCapacity) {
        this.brand = brand;
        this.model = model;
        this.condition = condition;
        this.price = price;
        this.productionYear = productionYear;
        this.mileage = mileage;
        this.engineCapacity = engineCapacity;
    }


    public void print(){
        System.out.println("Information's about vehicle");
        System.out.println("Brand: "+brand);
        System.out.println("Model: "+model);
        System.out.println("Condition: "+condition);
        System.out.println("Price: "+price);
        System.out.println("Produced in: "+productionYear);
        System.out.println("Mileage: "+mileage);
        System.out.println("Capacity of engine: "+engineCapacity);
    }


    public int compare(Vehicle other) {
        return this.brand.compareTo(other.brand);
    }

    public String getBrand() {
        return brand;
    }

    public String getModel() {
        return model;
    }

    public ItemCondition getCondition() {
        return condition;
    }

    public double getPrice() {
        return price;
    }

    public int getProductionYear() {
        return productionYear;
    }

    public double getMileage() {
        return mileage;
    }

    public double getEngineCapacity() {
        return engineCapacity;
    }

    @Override
    public int compareTo(Vehicle o) {
        return 0;
    }}


