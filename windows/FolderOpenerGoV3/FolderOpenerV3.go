package main

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"strings"

	"github.com/energye/systray"
	"github.com/tawesoft/golib/v2/dialog"
)

const (
	CONN_HOST = "0.0.0.0"
	CONN_PORT = "9997"
	CONN_TYPE = "tcp"
)

var toolTip = ""
var timeToQuit = false

func main() {
	runServer()
}

func addQuitItem() {
	mQuit := systray.AddMenuItem("Quit", "Quit the whole app")
	mQuit.Enable()
	mQuit.Click(func() {
		systray.Quit()
	})
}

func onReady() {
	systray.SetIcon(icon)
	systray.SetTooltip(toolTip)
	addQuitItem()
}

func onExit() {
	timeToQuit = true
	os.Exit(0)
}

// //////////////////////////////////////////////

func runServer() bool {
	if len(os.Args) != 2 {
		dialog.Alert("Usage: %s SOURCE_IP_PREFIX", os.Args[0])
		return false
	}
	l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		dialog.Alert("Error listening: %s", err.Error())
		return false
	}
	// Close the listener when the application closes.
	defer l.Close()

	toolTip = fmt.Sprintf("FolderOpener: Port %s, prefix %s", CONN_PORT, os.Args[1])

	go systray.Run(onReady, onExit)

	for {
		// Listen for an incoming connection.
		conn, err := l.Accept()
		if err != nil {
			dialog.Alert("Error accepting: ", err.Error())
			os.Exit(1)
			return false
		}
		if timeToQuit {
			return true
		}
		// Handle connections in a new goroutine.
		go handleRequest(conn)
	}
	return true
}

func sanityzeString(inputString string) string {
	newString := strings.Replace(inputString, "\n", "", -1)
	newString = strings.Replace(newString, "\r", "", -1)
	newString = strings.Trim(newString, " ")

	for {
		if !strings.Contains(newString, "  ") {
			break
		}
		newString = strings.Replace(newString, "  ", " ", -1)
	}

	return newString
}

func execHelper(cmd_string string) *exec.Cmd {
	cmd_array := strings.Split(cmd_string, " ")
	cmd_array_len := len(cmd_array)

	if cmd_array_len == 1 {
		return exec.Command(cmd_array[0])
	}

	if cmd_array_len == 2 {
		return exec.Command(cmd_array[0], cmd_array[1])
	}

	if cmd_array_len == 3 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2])
	}

	if cmd_array_len == 4 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3])
	}

	if cmd_array_len == 5 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4])
	}

	if cmd_array_len == 6 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5])
	}

	if cmd_array_len == 7 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6])
	}

	if cmd_array_len == 8 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7])
	}

	if cmd_array_len == 9 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8])
	}

	if cmd_array_len == 10 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9])
	}

	if cmd_array_len == 11 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10])
	}

	if cmd_array_len == 12 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11])
	}

	if cmd_array_len == 13 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12])
	}

	if cmd_array_len == 14 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13])
	}

	if cmd_array_len == 15 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14])
	}

	if cmd_array_len == 16 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15])
	}

	if cmd_array_len == 17 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16])
	}

	if cmd_array_len == 18 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17])
	}

	if cmd_array_len == 19 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18])
	}

	if cmd_array_len == 20 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19])
	}

	if cmd_array_len == 21 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20])
	}

	if cmd_array_len == 22 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21])
	}

	if cmd_array_len == 23 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22])
	}

	if cmd_array_len == 24 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23])
	}

	if cmd_array_len == 25 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23], cmd_array[24])
	}

	if cmd_array_len == 26 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23], cmd_array[24], cmd_array[25])
	}

	if cmd_array_len == 27 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23], cmd_array[24], cmd_array[25], cmd_array[26])
	}

	if cmd_array_len == 28 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23], cmd_array[24], cmd_array[25], cmd_array[26], cmd_array[27])
	}

	if cmd_array_len == 29 {
		return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23], cmd_array[24], cmd_array[25], cmd_array[26], cmd_array[27], cmd_array[28])
	}

	return exec.Command(cmd_array[0], cmd_array[1], cmd_array[2], cmd_array[3], cmd_array[4], cmd_array[5], cmd_array[6], cmd_array[7], cmd_array[8], cmd_array[9], cmd_array[10], cmd_array[11], cmd_array[12], cmd_array[13], cmd_array[14], cmd_array[15], cmd_array[16], cmd_array[17], cmd_array[18], cmd_array[19], cmd_array[20], cmd_array[21], cmd_array[22], cmd_array[23], cmd_array[24], cmd_array[25], cmd_array[26], cmd_array[27], cmd_array[28], cmd_array[29])

}

func runCommand(source_ip string, cmd_string string) {

	if len(cmd_string) == 0 {
		return
	}

	// fmt.Println(fmt.Sprintf("->[%s]->[%s]", source_ip, cmd_string))

	// systray.SetTooltip(fmt.Sprintf("%s [%s]->[%s]", toolTip, source_ip, cmd_string))
	execHelper(cmd_string).Output()
	// cmd := execHelper(cmd_string)
	// stdout, err := cmd.Output()

	// if err != nil {
	// 	fmt.Println(err.Error())
	// 	return
	// }

	// // Print the output
	// fmt.Println(string(stdout))

	// if err := cmd.Run(); err != nil {
	// 	log.Fatal(err)
	// }

	// fmt.Println(fmt.Sprintf("<-[%s]", sanityzeString(string(stdout))))
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

			runCommandIfSafe(source_ip, cmd_string)

		} else {
			fmt.Println("Ignoring request from non whitelisted IP [", source_ip, "]")
		}
	}
	conn.Close()
}

func runCommandIfSafe(source_ip string, cmd_string string) {
	unsafeCommands := []string{"rm ", "cmd ", "echo ", "del ", "GET ", "POST ", "HEAD ", "PUT ", "OPTIONS ", "PATCH "}
	unsafeChars := []string{">", "<", "=", "|", ";"}

	for _, unsafeCommand := range unsafeCommands {
		if strings.HasPrefix(cmd_string, unsafeCommand) {
			fmt.Println("Ignoring dangerous command [", cmd_string, "]")
			return
		}
	}

	for _, unsafeChar := range unsafeChars {
		if strings.Contains(cmd_string, unsafeChar) {
			fmt.Println("Ignoring dangerous command [", cmd_string, "]")
			return
		}
	}
	runCommand(source_ip, cmd_string)
}
