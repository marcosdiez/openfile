using System;
using System.Text;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.IO;

namespace FolderOpener2
{

    public partial class MainWindow : Form
    {
        int port = 9998;
        string allowedIp = "";

        private Socket socket;
        private Thread thread;

        private NetworkStream networkStream;
        private BinaryWriter binaryWriter;
        private LineReader binaryReader;

        public MainWindow()
        {
            InitializeComponent();
            this.WindowState = FormWindowState.Minimized;
            mimimizeMe();
            thread = new Thread(new ThreadStart(RunServer));
            thread.Start();
        }

        public void updInfo(String textLog)
        {
            if (this.txtStatus.InvokeRequired)
            {
                txtStatus.Invoke(new MethodInvoker(delegate
                {
                    txtStatus.Text += textLog + "\r\n";
                    txtStatus.SelectionStart = txtStatus.Text.Length;
                    txtStatus.ScrollToCaret();
                    txtStatus.Refresh();
                }));
            }
            else
            {
                this.txtStatus.Text = textLog;
            }
        }

        bool isAuthorized(Socket socket)
        {
            var ip = getIp(socket);
            if (ip == allowedIp)
                return true;

            var result = MessageBox.Show(
                "Would you like to accept incoming connections from " + ip + " ?",
                "Folder Opener", MessageBoxButtons.YesNo);

            if (result == DialogResult.Yes)
            {
                //StatusBarLabel.Text = "Allowed IP: " + ip;
                allowedIp = ip;
                return true;
            }
            return false;
        }

        string getIp(Socket socket)
        {
            var connection = socket.RemoteEndPoint.ToString();
            var pos = connection.IndexOf(":");
            if (pos <= 0)
            {
                return connection;
            }
            var ip = connection.Substring(0, pos);
            return ip;
        }

        public void RunServer()
        {
            TcpListener tcpListener;
            try
            {
                var ipEndPoint = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
                tcpListener = new TcpListener(ipEndPoint);
                tcpListener.Start();

                updInfo("We are listening to port " + port);

                while (true)
                {
                    socket = tcpListener.AcceptSocket();
                    if (isAuthorized(socket))
                    {
                        (new Thread(new ThreadStart(ProcessConnection))).Start();
                    }
                    else
                    {
                        updInfo("Ignored: [" + socket.RemoteEndPoint + "]");
                        socket.Close();
                    }

                }
            }
            catch (Exception ex) //Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                if (binaryReader != null)
                {
                    binaryReader.Close();
                }
                if (binaryWriter != null)
                {
                    binaryWriter.Close();
                }
                if (networkStream != null)
                {
                    networkStream.Close();
                }
                if (socket != null)
                {
                    socket.Close();
                }
                updInfo("Conection Terminated");
            }
        }

        void ProcessConnection()
        {
            networkStream = new NetworkStream(socket);
            binaryWriter = new BinaryWriter(networkStream);
            binaryReader = new LineReader(networkStream, Encoding.UTF8);

            // updInfo("conexão recebida!");
            // binaryWriter.Write("\nconexão efetuada!");

            string messageReceived = "";
            do
            {
                messageReceived = binaryReader.ReadLine();
                if (String.IsNullOrEmpty(messageReceived))
                {
                    socket.Close();
                }
                else
                {
                    var ip = socket.RemoteEndPoint.ToString();
                    runRemoteCommand(messageReceived);
                    updInfo("[" + ip + ": " + messageReceived + "]");
                }
            } while (socket.Connected);
        }

        void runRemoteCommand(string messageReceived)
        {
            if (String.IsNullOrEmpty(messageReceived))
            {
                return;
            }
            messageReceived = messageReceived.Trim();

            ExecuteCommandSync("start " + messageReceived);
        }
       
        void ExecuteCommandSync(object command)
        {
            updInfo(command.ToString());
            try
            {
                // create the ProcessStartInfo using "cmd" as the program to be run,
                // and "/c " as the parameters.
                // Incidentally, /c tells cmd that we want it to execute the command that follows,
                // and then exit.
                System.Diagnostics.ProcessStartInfo procStartInfo =
                    new System.Diagnostics.ProcessStartInfo("cmd", "/c " + command);

                // The following commands are needed to redirect the standard output.
                // This means that it will be redirected to the Process.StandardOutput StreamReader.
                procStartInfo.RedirectStandardOutput = true;
                procStartInfo.UseShellExecute = false;
                // Do not create the black window.
                procStartInfo.CreateNoWindow = true;
                // Now we create a process, assign its ProcessStartInfo and start it
                System.Diagnostics.Process proc = new System.Diagnostics.Process();
                proc.StartInfo = procStartInfo;
                proc.Start();
                // Get the output into a string
                string result = proc.StandardOutput.ReadToEnd();
                // Display the command output.
                Console.WriteLine(result);
            }
            catch (Exception) // objException)
            {
                // Log the exception
            }
        }

        private void MainWindow_FormClosed(object sender, FormClosedEventArgs e)
        {
            myNotifyIcon.Visible = false;
            Environment.Exit(0);
        }

        void mimimizeMe()
        {
            myNotifyIcon.Visible = true;
            this.ShowInTaskbar = false;
            this.Hide();
        }

        private void MainWindow_Resize(object sender, EventArgs e)
        {
            if (FormWindowState.Minimized == this.WindowState)
            {
                mimimizeMe();
            }

            else if (FormWindowState.Normal == this.WindowState)
            {
                myNotifyIcon.Visible = false;
                this.ShowInTaskbar = true;
            }
        }

        private void myNotifyIcon_DoubleClick(object sender, EventArgs e)
        {
            this.Show();
            this.WindowState = FormWindowState.Normal;
        }

    }

}