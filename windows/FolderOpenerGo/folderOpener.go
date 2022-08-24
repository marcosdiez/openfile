package main

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"strings"
)

const (
	CONN_HOST = "0.0.0.0"
	CONN_PORT = "9997"
	CONN_TYPE = "tcp"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: ", os.Args[0], "SOURCE_IP_PREFIX")
		os.Exit(1)
	}
	fmt.Println("Source IP prefix:", os.Args[1])
	// Listen for incoming connections.
	l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	// Close the listener when the application closes.
	defer l.Close()
	fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)
	for {
		// Listen for an incoming connection.
		conn, err := l.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		// Handle connections in a new goroutine.
		go handleRequest(conn)
	}
}

func sanityzeString(inputString string) string {
	newString := strings.Replace(inputString, "\n", "", -1)
	newString = strings.Replace(newString, "\r", "", -1)
	newString = strings.Trim(newString, " ")
	return newString
}

func runCommand(source_ip string, cmd_string string) {

	if len(cmd_string) == 0 {
		return
	}

	fmt.Println(fmt.Sprintf("->[%s]->[%s]", source_ip, cmd_string))
	cmd_array := strings.Split(cmd_string, " ")
	cmd_array_len := len(cmd_array)

	cmd := exec.Command("")

	if cmd_array_len == 1 {
		cmd = exec.Command(cmd_array[0])
	}
	if cmd_array_len == 2 {
		cmd = exec.Command(cmd_array[0], cmd_array[1])
	}
	if cmd_array_len == 3 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2])
	}
	if cmd_array_len == 4 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3])
	}
	if cmd_array_len == 5 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4])
	}
	if cmd_array_len == 6 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5])
	}
	if cmd_array_len == 7 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6])
	}
	if cmd_array_len == 8 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7])
	}
	if cmd_array_len >= 9 {
		cmd = exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8])
	}

	stdout, err := cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return
	}

	// // Print the output
	// fmt.Println(string(stdout))

	// if err := cmd.Run(); err != nil {
	// 	log.Fatal(err)
	// }

	fmt.Println(fmt.Sprintf("<-[%s]", string(stdout)))
}

// Handles incoming requests.
func handleRequest(conn net.Conn) {
	if addr, ok := conn.RemoteAddr().(*net.TCPAddr); ok {
		source_ip := addr.IP.String()

		if strings.HasPrefix(source_ip, os.Args[1]) {
			// Make a buffer to hold incoming data.
			buf := make([]byte, 10240)
			// Read the incoming connection into the buffer.
			reqLen, err := conn.Read(buf)
			if err != nil {
				fmt.Println("Error reading ", reqLen, " bytes: ", err.Error())
			}
			// Send a response back to person contacting us.
			conn.Write([]byte("Message received.\n"))
			// fmt.Println("[", buf, "]")

			cmd_string := sanityzeString(string(buf[:reqLen]))

			runCommand(source_ip, cmd_string)
		} else {
			fmt.Println("Ignoring request from evil IP [", source_ip, "]")
		}
	}
	conn.Close()
}
