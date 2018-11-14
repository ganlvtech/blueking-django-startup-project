package main

import (
    "fmt";
    "time";
)

func main() {
    fmt.Println("Hello, gopher!");
    time.Sleep(5 * time.Second);
    fmt.Println("Hello, I'm back!");
}
