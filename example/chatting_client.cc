// Demonstrate the use of "select" to implement a multiple socket manager
// George F. Riley, Georgia Tech, Spring 2010

// This is the client side

#include <stdio.h>
#include <iostream>
#include <vector>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

int main(int argc, char** argv)
{
  struct addrinfo hints, *res, *p;
  int status;
  if (argc < 2)
    {
      cout << "Usage: chat hostname" << endl;
      exit(1);
    }
  
  
  /*
  struct hostent* pHE = gethostbyname(argv[1]);
  if (pHE == 0)
    { // not found
      cout << "Can't find IP address for host " << argv[1] << endl;
      exit(2);
    }
    */  
  memset(&hints, 0, sizeof(hints));
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;

  const char* port = "2000"; // Arbitrarily chosen port number
  //if (argc > 2) port = argv[2];

  if ((status = getaddrinfo(argv[1], port, &hints, &res)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        return 1;
  }
  
  int sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);


  /*
  struct sockaddr_in sockAddr;
  sockAddr.sin_family = AF_INET;
  // Get the ip address from the hostent structure
  memcpy(&sockAddr.sin_addr, pHE->h_addr, 4);
  unsigned short port = 2000; // Arbitrarily chosen port number
  if (argc > 2) port = atol(argv[2]);
  sockAddr.sin_port = htons(port);
  */

  // Create socket and bind
  if (connect(sockfd, res->ai_addr, res->ai_addrlen) < 0)
    {
      std::cout << "connect failed" << std::endl;
      exit(1);
    }
  while(true)
    {
      // We need to use select to read either from standard in (handle = 1)
      // or the socket
      fd_set readSet;
      fd_set errorSet;
      FD_ZERO(&readSet);
      FD_ZERO(&errorSet);
      // Set two bits in the readSet bitmap, standard in and the socket
      FD_SET(STDIN_FILENO, &readSet);
      FD_SET(STDIN_FILENO, &errorSet);
      FD_SET(sockfd, &readSet);
      FD_SET(sockfd, &errorSet);
      // here we don't use the write set or the time outvalue
      select(sockfd + 1, &readSet, 0, &errorSet, 0);
      if (FD_ISSET(sockfd, &readSet) || 
          FD_ISSET(sockfd, &errorSet))
        { // Read from socket
          char buf[10000];
          int actual = read(sockfd, buf, sizeof(buf));
          if (actual <= 0) break; // Remote closed connection
          // write the data to standard out     
          write(STDOUT_FILENO, buf, actual);
        }
        if (FD_ISSET(STDIN_FILENO, &readSet) || 
            FD_ISSET(STDIN_FILENO, &errorSet))
        { // Data available from keyboard
          char buf[10];
          int actual = read(STDIN_FILENO, buf, sizeof(buf));
          if (actual <= 0) break;  // End of file
          // Write to socket
          int wrote = write(sockfd, buf, actual);
        }
    }
  close(sockfd);
}
