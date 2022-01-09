package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func readWords(file_name *string) (forbidden_words map[string]bool) {
	file, err := os.Open(*file_name)
	if err != nil {
		log.Fatal((err))
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanWords)
	forbidden_words = make(map[string]bool)
	for scanner.Scan() {
		forbidden_words[strings.ToLower(scanner.Text())] = true
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return
}
func printForbiddenWords(forbidden_words *map[string]bool) {
	for forbidden_word := range *forbidden_words {
		fmt.Println(forbidden_word)
	}
}

func checkWord(word *string, forbidden_words *map[string]bool) bool {
	if _, ok := (*forbidden_words)[strings.ToLower(*word)]; ok {
		return true
	}
	return false
}

func wordToStars(word *string) string {
	return strings.Repeat("*", len(*word))
}
func main() {
	var file_name string
	fmt.Scanf("%s", &file_name)
	var forbidden_words map[string]bool
	forbidden_words = readWords(&file_name)
	var wordForCheck string
	for fmt.Scanf("%s", &wordForCheck); strings.ToLower(wordForCheck) != "exit"; {
		if isWordForbidden := checkWord(&wordForCheck, &forbidden_words); isWordForbidden {
			fmt.Println(wordToStars(&wordForCheck))
		} else {
			fmt.Println(wordForCheck)
		}
		fmt.Scanf("%s", &wordForCheck)
	}
	fmt.Println("Bye!")
}
