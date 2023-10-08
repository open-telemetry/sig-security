# why the SECURITY SIG to bind to localhost
Binding to "localhost" restricts the service to only accept connections from the local machine, making it less accessible to potential attackers on the network. On the 
other hand, binding to "0.0.0.0" would make the service listen on all available network interfaces,potentially exposing it to external connections, which can be a 
security risk if not properly configured and secured.

   # Binding to "localhost" (127.0.0.1):
    Limits the service to accept connections only from the local machine.
    Provides a higher level of security as external connections are not allowed by default.
    Recommended for services that don't need to be accessed over the network.

   # Binding to "0.0.0.0":
    Makes the service listen on all available network interfaces.
    Allows connections from any external source, which can pose a security risk if not properly configured.
    Typically used when you want the service to be accessible over the network, but additional security measures (e.g., firewalls, access controls) are needed to 
    secure it
.
Binding with localhost aligns with security best practices to minimize exposure to potential threats. 
