// Demonstrate the use of "select" to implement a multiple socket manager
// George F. Riley, Georgia Tech, Spring 2010

// This is the server side

#include <iostream>
#include <vector>

#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

vector<int> clientSockets;  // Maintains a collection of client socket numbers

int main(int argc, char** argv)
{
  struct sockaddr_in sockAddr;
  sockAddr.sin_family = AF_INET;
  sockAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  unsigned short port = 2000; // Arbitrarily chosen port number
  if (argc > 1) port = atol(argv[1]); // Port from command line
  sockAddr.sin_port = htons(port);
  
  // Create socket and bind
  int listenSock = socket(AF_INET, SOCK_STREAM, 0);
  if (bind(listenSock, (struct sockaddr*)&sockAddr, sizeof(sockAddr)) < 0)
    {
      std::cout << "Bind failed" << std::endl;
      exit(1);
    }
  listen(listenSock, 5);
  
  while(true)
    {
      fd_set readSet;
      fd_set writeSet;
      fd_set errorSet;
      // Clear all bits to zero
      FD_ZERO(&readSet);
      FD_ZERO(&writeSet);
      FD_ZERO(&errorSet);
      // Now set the read bit for the listening socket
      int maxSock = listenSock;
      FD_SET(listenSock, &readSet);
      // Set the read bits for each client socket
      for (unsigned i = 0; i < clientSockets.size(); ++i)
        {
          if (clientSockets[i] < 0) continue; // No longer used
          if (clientSockets[i] > maxSock) maxSock = clientSockets[i];
          FD_SET(clientSockets[i], &readSet);
        }
      struct timeval t; // This specifies wait time
      t.tv_sec = 10;     // Wait for ten seconds
      t.tv_usec = 0;
      select(maxSock + 1, &readSet, &writeSet, &errorSet, &t);
      // See if listening socket can be "read", ie. call accept
      //cout << "After select" << endl;
      
      if (FD_ISSET(listenSock, &readSet))
        {
          int s = accept(listenSock, 0, 0);
          //cout << "Got accept, socket " << s << endl;
          clientSockets.push_back(s);
        }
      // Check each client for input data
      char buf[10000];
      for (unsigned i = 0; i < clientSockets.size(); ++i)
        {
          if (clientSockets[i] < 0) continue; // No longer used
          if (FD_ISSET(clientSockets[i], &readSet) ||
              FD_ISSET(clientSockets[i], &errorSet))
            {
              //cout << "Reading socket " << clientSockets[i] << endl;
              int actual = read(clientSockets[i], buf, sizeof(buf));
              //cout << "Got " << actual << " bytes" << endl;
              if (actual <= 0)
                { // Closed or error
                  //cout << "Remote closed socket " << clientSockets[i]
                  //     << endl;
                  close(clientSockets[i]);
                  clientSockets[i] = -1; // Note no longer used
                }
              else
                {
                  // And echo this data to each client
                  for (unsigned j = 0; j < clientSockets.size(); ++j)
                    {
                      if (clientSockets[j] < 0) continue;
                      if(i == j) continue;
                      int wrote = write(clientSockets[j], buf, actual);
                      //cout << "Wrote " << wrote << " bytes to socket "
                      //     <<  clientSockets[i] << endl;
                    }
                }
            }
        }
    }
}
