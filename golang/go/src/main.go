package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("Hello, gopher!")
	t0 := time.Now()
	for {
		t := time.Now()
		dt := t.Sub(t0)
		fmt.Println(dt)
		time.Sleep(50 * time.Millisecond)
		if dt > 5 * time.Second {
			break
		}
	}
	fmt.Println("Hello, I'm back!")
}
