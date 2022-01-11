package main

import (
	"fmt"
	"log"
)

type CoffeeCup struct {
	water  int
	milk   int
	coffee int
	price  int
}
type CoffeeMachine struct {
	money          int
	water          int
	milk           int
	coffee         int
	disposableCups int
	coffeeCups     map[string]CoffeeCup
}

func getUserInt() (userInput int) {
	_, err := fmt.Scanf("%d", &userInput)
	if err != nil {
		log.Fatal(err)
	}
	return userInput
}
func (coffeeMachine *CoffeeMachine) printState() {
	fmt.Printf(`The coffee machine has:
%d of water
%d of milk
%d of coffee beans
%d of disposable cups
%d of money
`, coffeeMachine.water, coffeeMachine.milk, coffeeMachine.coffee, coffeeMachine.disposableCups, coffeeMachine.money)
}
func (coffeeMachine *CoffeeMachine) makeCoffee(coffeeType string) {
	if coffeeMachine.coffeeCups[coffeeType].water > coffeeMachine.water {
		fmt.Println("Sorry, not enough water!")
		return
	}
	if coffeeMachine.coffeeCups[coffeeType].milk > coffeeMachine.milk {
		fmt.Println("Sorry, not enough milk!")
		return
	}
	if coffeeMachine.coffeeCups[coffeeType].coffee > coffeeMachine.coffee {
		fmt.Println("Sorry, not enough coffee beans!")
		return
	}
	if coffeeMachine.disposableCups < 1 {
		fmt.Println("Sorry, not enough disposable cups!")
		return
	}
	coffeeMachine.water -= coffeeMachine.coffeeCups[coffeeType].water
	coffeeMachine.milk -= coffeeMachine.coffeeCups[coffeeType].milk
	coffeeMachine.coffee -= coffeeMachine.coffeeCups[coffeeType].coffee
	coffeeMachine.money += coffeeMachine.coffeeCups[coffeeType].price
	coffeeMachine.disposableCups--
	fmt.Println("I have enough resources, making you a coffee!")
}
func (coffeeMachine *CoffeeMachine) buyCoffee() {
	fmt.Println("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
	var userInput string
	fmt.Scanln(&userInput)
	switch userInput {
	case "1":
		coffeeMachine.makeCoffee("espresso")
	case "2":
		coffeeMachine.makeCoffee("latte")
	case "3":
		coffeeMachine.makeCoffee("cappuccino")
	case "back":
		return
	}
}
func addUserIntInput(question string, value *int) {
	fmt.Println(question)
	var additionalValue int = getUserInt()
	*value = *value + additionalValue
}
func (coffeeMachine *CoffeeMachine) fillIngredients() {
	addUserIntInput("Write how many ml of water you want to add:", &coffeeMachine.water)
	addUserIntInput("Write how many ml of milk you want to add:", &coffeeMachine.milk)
	addUserIntInput("Write how many grams of coffee beans you want to add:", &coffeeMachine.coffee)
	addUserIntInput("Write how many disposable coffee cups you want to add:", &coffeeMachine.disposableCups)

}
func (coffeeMachine *CoffeeMachine) takeMoney() {
	fmt.Printf("I gave you $%d\n", coffeeMachine.money)
	coffeeMachine.money = 0
}
func newInitCoffeeMachine() CoffeeMachine {
	coffeeCups := make(map[string]CoffeeCup)
	coffeeCups["espresso"] = CoffeeCup{
		water:  250,
		milk:   0,
		coffee: 16,
		price:  4}
	coffeeCups["latte"] = CoffeeCup{
		water:  350,
		milk:   75,
		coffee: 20,
		price:  7}
	coffeeCups["cappuccino"] = CoffeeCup{
		water:  200,
		milk:   100,
		coffee: 12,
		price:  6}
	return CoffeeMachine{
		water:          400,
		milk:           540,
		coffee:         120,
		disposableCups: 9,
		money:          550,
		coffeeCups:     coffeeCups,
	}
}
func buyFillTake() {
	var coffeeMachine CoffeeMachine = newInitCoffeeMachine()
	for {
		fmt.Println("Write action (buy, fill, take, remaining, exit):")
		var userChoice string
		fmt.Scanf("%s", &userChoice)
		switch userChoice {
		case "buy":
			coffeeMachine.buyCoffee()
		case "fill":
			coffeeMachine.fillIngredients()
		case "take":
			coffeeMachine.takeMoney()
		case "remaining":
			coffeeMachine.printState()
		case "exit":
			return

		}
	}
}
func main() {
	buyFillTake()
}
