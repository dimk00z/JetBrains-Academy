package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func readWords(file_name *string) (forbidden_words []string) {
	file, err := os.Open(*file_name)
	if err != nil {
		log.Fatal((err))
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanWords)
	for scanner.Scan() {
		forbidden_words = append(forbidden_words, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return
}
func printForbiddenWords(forbidden_words *[]string) {
	for _, forbidden_word := range *forbidden_words {
		fmt.Println(forbidden_word)
	}
}
func main() {
	var file_name string
	fmt.Scan(&file_name)
	var forbidden_words []string
	forbidden_words = readWords(&file_name)
	printForbiddenWords(&forbidden_words)
}
