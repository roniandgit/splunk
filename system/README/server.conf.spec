#   Version 7.2.4.2
############################################################################
# This file contains settings and values to configure server options 
# in server.conf.
#
# There is a server.conf in $SPLUNK_HOME/etc/system/default/. To set custom
# configurations, place a copy of server.conf in 
# $SPLUNK_HOME/etc/system/local/.
#
# For examples, see server.conf.example. You must restart Splunk to enable
# configurations.
#
# To learn more about configuration files (including how file precedence is 
# determined) see the Administration Manual section about configuration 
# files. Splunk documentation can be found at 
# https://docs.splunk.com/Documentation.

# GLOBAL SETTINGS
# Use the [default] stanza to define any global settings.
#   * You can also define global settings outside of any stanza at the top
#     of the file.
#   * Each configuration file should have at most one default stanza. 
#     If you have multiple default stanzas, settings are combined. If you 
#     have multiple definitions of the same settings, the last definition 
#     in the file wins.
#   * If a setting is defined at both the global level and in a specific
#     stanza, the value in the specific stanza takes precedence.

############################################################################
# General Server Configuration
############################################################################
[general]
serverName = <ASCII string>
* The name that identifies this Splunk software instance for features such as
  distributed search.
* Cannot be an empty string.
* Can contain environment variables.
* After any environment variables are expanded, the server name
  (if not an IPv6 address) can only contain letters, numbers, underscores,
  dots, and dashes. The server name must start with a letter, number, or an
  underscore.
* Default: <hostname>-<user_running_splunk>

hostnameOption = <ASCII string>
* This option lets you specify the details in the server name that 
  identifies this Splunk instance.
* Applies to Windows only.
* Can be one of the following: "fullyqualifiedname", "clustername", "shortname".
* Cannot be an empty string.

sessionTimeout = <nonnegative integer>[s|m|h|d]
* The amount of time before a user session times out, expressed as a
  search-like time range.
* Examples include "24h" (24 hours), "3d" (3 days),
  "7200s" (7200 seconds, or two hours)
* Default: "1" (1 hour)

trustedIP = <IP address>
* All logins from specified IP addresses are trusted. This means a 
  password is no longer required.
* Only set this if you are using Single Sign-On (SSO).

allowRemoteLogin = always|never|requireSetPassword
* Controls remote management by restricting general login. Note that this
  does not apply to trusted SSO logins from a trustedIP.
* If set to "always", enables authentication so that all remote login attempts
  are allowed.
* If set to "never", only local logins to splunkd are allowed. Note that this
  still allows remote management through splunkweb, if splunkweb is on
  the same server.
* If  set to "requireSetPassword", which is the default:
  * In the free license, remote login is disabled.
  * In the pro license, remote login is only disabled for "admin" user if
    the default password of "admin" has not been changed.
* NOTE: As of version 7.1, Splunk software does not support the use of default 
  passwords.

tar_format = gnutar|ustar
* Sets the default TAR format.
* Default: gnutar

access_logging_for_phonehome = <boolean>
* Enables/disables logging to the splunkd_access.log file for client phonehomes.
* Default: true (logging enabled)

hangup_after_phonehome = <boolean>
* Controls whether or not the deployment server hangs up the connection
  after the phonehome is done.
* By default, persistent HTTP 1.1 connections are used with the server to
  handle phonehomes. This might show higher memory usage if you have a large 
  number of clients.
* If you have more than the maximum concurrent tcp connection number of
  deployment clients, persistent connections do not help with the reuse of
  connections. In which case setting this to false helps bring down memory
  usage.
* Default: false (persistent connections for phonehome)

pass4SymmKey = <password>
* Authenticates traffic between:
  * License master and its license slaves.
  * Members of a cluster; see Note 1 below.
  * Deployment server (DS) and its deployment clients (DCs); see Note 2
    below.
* Note 1: Clustering might override the passphrase specified here, in
  the [clustering] stanza. A clustering searchhead connecting to multiple
  masters might further override in the [clustermaster:stanza1] stanza.
* Note 2: By default, DS-DCs passphrase authentication is disabled. 
  To enable DS-DCs passphrase authentication, you must *also* add the 
  following line to the [broker:broker] stanza in the restmap.conf file:
     requireAuthentication = true
* In all scenarios, *every* node involved must set the same passphrase in
  the same stanzas. For example in the [general] stanza and/or 
  [clustering] stanza.
  Otherwise, the respective communication:
    - licensing and deployment in the case of the [general] stanza
    - clustering in case of the [clustering] stanza) 
  does not proceed.
* Unencrypted passwords must not begin with "$1$", as this is used by
  Splunk software to determine if the password is already encrypted.

listenOnIPv6 = no|yes|only
* By default, splunkd listens for incoming connections (both REST and
  TCP inputs) using IPv4 only.
* When you set this value to "yes", splunkd simultaneously listens for 
  connections on both IPv4 and IPv6.
* To disable IPv4 entirely, set listenOnIPv6 to "only". This causes splunkd
  to exclusively accept connections over IPv6. You might need to change 
  the mgmtHostPort setting in the web.conf file. 
  Use '[::1]' instead of '127.0.0.1'.
* Any setting of SPLUNK_BINDIP in your environment or the 
  splunk-launch.conf file overrides the listenOnIPv6 value. 
  In this case splunkd listens on the exact address specified.

connectUsingIpVersion = auto|4-first|6-first|4-only|6-only
* When making outbound TCP connections for forwarding event data, making
  distributed search requests, etc., this setting controls whether the 
  connections are made using IPv4 or IPv6.
* Connections to literal addresses are unaffected by this setting. For
  example, if a forwarder is configured to connect to "10.1.2.3" the
  connection is made over IPv4 regardless of this setting.
* "auto:" 
    * If listenOnIPv6 is set to "no", the Splunk server follows the 
      "4-only" behavior.  
    * If listenOnIPv6 is set to "yes", the Splunk server follows "6-first" 
    * If listenOnIPv6 is set to "only", the Splunk server follow 
      "6-only" behavior.
* "4-first:" If a host is available over both IPv4 and IPv6, then 
  the Splunk server connects over IPv4 first and falls back to IPv6 if the 
  connection fails.
* "6-first": splunkd tries IPv6 first and fallback to IPv4 on failure.
* "4-only": splunkd only attempts to make connections over IPv4.
* "6-only": splunkd only attempts to connect to the IPv6 address.
* Default: auto. This means that the Splunk server selects a reasonable value 
                 based on the listenOnIPv6 setting. 

guid = <globally unique identifier for this instance>
* This setting (as of version 5.0) belongs in the [general] stanza of
  SPLUNK_HOME/etc/instance.cfg file. See the .spec file of instance.cfg for
  more information.

useHTTPServerCompression = <boolean>
* Specifies whether the splunkd HTTP server should support gzip content 
  encoding. For more info on how content encoding works, see Section 14.3
  of Request for Comments: 2616 (RFC2616) on the World Wide Web Consortium
  (W3C) website.
* Default: true

defaultHTTPServerCompressionLevel = <integer>
* If the useHTTPServerCompression setting is enabled (which it is by default), 
  this setting controls the compression level that the Splunk server 
  attempts to use.
* This number must be between 1 and 9.
* Higher numbers produce smaller compressed results but require more CPU
  usage.
* Default: 6 (which is appropriate for most environments)

skipHTTPCompressionAcl = <network_acl>
* Lists a set of networks or addresses to skip data compression.
  These are addresses that are considered so close that network speed is
  never an issue, so any CPU time spent compressing a response is wasteful.
* Note that the server might still respond with compressed data if it
  already has a compressed version of the data available.
* These rules are separated by commas or spaces.
* Each rule can be in the following forms:
    1. A single IPv4 or IPv6 address, for example: "10.1.2.3", "fe80::4a3"
    2. A CIDR block of addresses, for example: "10/8", "fe80:1234/32"
    3. A DNS name, possibly with a '*' used as a wildcard, for example:
       "myhost.example.com", "*.splunk.com")
    4. A single '*' which matches anything
* Entries can also be prefixed with '!' to negate their meaning.
* Default: localhost addresses

legacyCiphers = decryptOnly|disabled
* This setting controls how Splunk software handles support for 
  legacy encryption ciphers.
* If set to "decryptOnly", Splunk software supports decryption of
  configurations that have been encrypted with legacy ciphers.
  It encrypts all new configurations with newer and stronger cyphers.
* If set to "disabled", Splunk software neither encrypts nor decrypts
  configurations that have been encrypted with legacy ciphers.
* Default: "decryptOnly".

site = <site-id>
* Specifies the site that this Splunk instance belongs to when multisite is
  enabled.
* Valid values for site-id include site0 to site63
* The special value "site0" can be set only on search heads or on forwarders 
  that are participating in indexer discovery.
  * For a search head, "site0" disables search affinity. 
  * For a forwarder participating in indexer discovery, "site0" causes the 
    forwarder to send data to all peer nodes across all sites.

useHTTPClientCompression = true|false|on-http|on-https
* Specifies whether gzip compression should be supported when Splunkd acts 
  as a client (including distributed searches). Note: For the content to
  be compressed, the HTTP server that the client is connecting to should
  also support compression.
* If the connection is being made over https and
  useClientSSLCompression=true, then setting useHTTPClientCompression=true
  results in double compression work without much compression gain. It
  is recommended that this value be set to "on-http" (or to "true", and
  useClientSSLCompression to "false").
* Default: false

embedSecret = <string>
* When using report embedding, normally the generated URLs can only
  be used on the search head that they were generated on.
* If "embedSecret" is set, then the token in the URL is encrypted
  with this key.  Then other search heads with the exact same setting
  can also use the same URL.
* This is needed if you want to use report embedding across multiple
  nodes on a search head pool.

parallelIngestionPipelines = <integer>
* The number of discrete data ingestion pipeline sets to create for this
  instance.
* A pipeline set handles the processing of data, from receiving streams
  of events through event processing and writing the events to disk.
* An indexer that operates multiple pipeline sets can achieve improved
  performance with data parsing and disk writing, at the cost of additional 
  CPU cores. 
* For most installations, the default setting of "1" is optimal. 
* Use caution when changing this setting. Increasing the CPU usage for data 
  ingestion reduces available CPU cores for other tasks like searching.
* NOTE: Enabling multiple ingestion pipelines can change the behavior of some
  settings in other configuration files. Each ingestion pipeline enforces 
  the limits of the following settings independently:
    1. maxKBps (in the limits.conf file)
    2. max_fd (in the limits.conf file)
    3. maxHotBuckets (in the indexes.conf file)
    4. maxHotSpanSecs (in the indexes.conf file)
* Default: 1

instanceType = <string>
* Should not be modified by users.
* Informs components (such as the SplunkWeb Manager section) which
  environment the Splunk server is running in, to allow for more 
  customized behaviors.
* Default: "download" which meanings no special behaviors

requireBootPassphrase = <boolean>
* Prompt the user for a boot passphrase when starting splunkd.
* Splunkd uses this passphrase to grant itself access to platform-provided
  secret storage facilities, like the GNOME keyring.
* For more information about secret storage, see the [secrets] stanza in
  $SPLUNK_HOME/etc/system/README/authentication.conf.spec.
* Default: true, if Common Criteria mode is enabled. False if 
  Common Criteria mode is disabled.

remoteStorageRecreateIndexesInStandalone = <boolean>
* Controls re-creation of remote storage enabled indexes in standalone mode.
* Default: true

cleanRemoteStorageByDefault = <boolean>
* Allows 'splunk clean eventdata' to clean the remote indexes when set to true.
* Default: false

recreate_index_fetch_bucket_batch_size = <positive_integer>
* Controls the maximum number of bucket IDs to fetch from remote storage
  as part of a single transaction for a remote storage enabled index.
* Only valid for standalone mode.
* Default: 500

recreate_bucket_fetch_manifest_batch_size = <positive_integer>
* Controls the maximum number of bucket manifests to fetch in parallel
  from remote storage.
* Only valid for standalone mode.
* Default: 100

splunkd_stop_timeout = <positive_integer>
* The maximum time, in seconds, that splunkd waits for a graceful shutdown to
  complete before splunkd forces a stop.
* Default: 360 (6 minutes)

############################################################################
# Deployment Configuration details
############################################################################

[deployment]
pass4SymmKey = <passphrase string>
    * Authenticates traffic between the deployment server (DS) and its 
      deployment clients (DCs).
    * By default, DS-DCs passphrase authentication key is disabled. To enable 
      DS-DCs passphrase authentication, you must *also* add the following 
      line to the [broker:broker] stanza in the restmap.conf file:
          requireAuthentication = true
    * If the key is not set in the [deployment] stanza, the key is looked 
      for in the [general] stanza.
    * NOTE: Unencrypted passwords must not begin with "$1$", because this is 
            used by Splunk software to determine if the password is already
            encrypted.

############################################################################
# SSL Configuration details
############################################################################

[sslConfig]
* Set SSL for communications on Splunk back-end under this stanza name.
  * NOTE: To set SSL (for example HTTPS) for Splunk Web and the browser, 
          use the web.conf file.
* Follow this stanza name with any number of the following attribute/value
  pairs.
* If you do not specify an entry for each attribute, the default value
  is used.

enableSplunkdSSL = <boolean>
* Enables/disables SSL on the splunkd management port (8089) and KV store
  port (8191).
* NOTE: Running splunkd without SSL is not generally recommended.
* Distributed search often performs better with SSL enabled.
* Default: true

useClientSSLCompression = <boolean>
* Turns on HTTP client compression.
* Server-side compression is turned on by default. Setting this on the
  client-side enables compression between server and client.
* Enabling this potentially gives you much faster distributed searches
  across multiple Splunk instances.
* Default: true

useSplunkdClientSSLCompression = <boolean>
* Controls whether SSL compression is used when splunkd is acting as
  an HTTP client, usually during certificate exchange, bundle replication,
  remote calls, etc.
* NOTE: This setting is effective if, and only if, useClientSSLCompression
        is set to "true".
* NOTE: splunkd is not involved in data transfer in distributed search, the
        search in a separate process is.
* Default: true

sslVersions = <versions_list>
* Comma-separated list of SSL versions to support for incoming connections.
* The versions available are "ssl3", "tls1.0", "tls1.1", and "tls1.2".
* The special version "*" selects all supported versions.  
  The version "tls"
  selects all versions tls1.0 or newer.
* If a version is prefixed with "-" it is removed from the list.
* SSLv2 is always disabled; "-ssl2" is accepted in the version list 
  but does nothing.
* When configured in FIPS mode, "ssl3" is always disabled regardless
  of this configuration.
* Default: The default can vary. See the 'sslVersions' setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  curent default.

sslVersionsForClient = <versions_list>
* Comma-separated list of SSL versions to support for outgoing HTTP connections
  from splunkd.  This includes distributed search, deployment client, etc.
* This is usually less critical, since SSL/TLS always picks the highest
  version both sides support.  However, you can use this setting to prohibit 
  making connections to remote servers that only support older protocols.
* The syntax is the same as the 'sslVersions' setting above.
* NOTE: For forwarder connections, there is a separate 'sslVersions'
  setting in the outputs.conf file. For connections to SAML servers, there 
  is a separate 'sslVersions' setting in the authentication.conf file.
* Default: The default can vary. See the 'sslVersionsForClient' setting in
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

supportSSLV3Only = <boolean>
* DEPRECATED.  SSLv2 is disabled.  The exact set of SSL versions
  allowed is configurable using the 'sslVersions' setting above.

sslVerifyServerCert = <boolean>
* This setting is used by distributed search and distributed 
  deployment clients.
     * For distributed search: Used when making a search request 
to another server in the search cluster.
     * For distributed deployment clients: Used when polling a 
       deployment server.
* If set to true, you should make sure that the server that is
  being connected to is a valid one (authenticated).  Both the common
  name and the alternate name of the server are then checked for a
  match if they are specified in this configuration file.  A
  certificate is considered verified if either is matched.
* Default: false

sslCommonNameToCheck = <commonName1>, <commonName2>, ...
* If set, and 'sslVerifyServerCert' is set to true,
  splunkd limits most outbound HTTPS connections to hosts which use
  a certificate with one of the listed common names.
* The most important scenario is distributed search.
* This feature does not work with the deployment server and client
  communication over SSL.
* Optional.  
* Default: No common name checking.

sslCommonNameList = <commonName1>, <commonName2>, ...
* DEPRECATED. Use the 'sslCommonNameToCheck' setting instead.

sslAltNameToCheck = <alternateName1>, <alternateName2>, ...
* If this value is set, and 'sslVerifyServerCert' is set to true,
  splunkd also verifies certificates which have a so-called 
  "Subject Alternate Name" that matches any of the alternate
  names in this list.
  * Subject Alternate Names are effectively extended descriptive
    fields in SSL certificates beyond the commonName.  A common 
    practice for HTTPS certificates is to use these values to store 
    additional valid hostnames or domains where the certificate 
    should be considered valid.
* Accepts a comma-separated list of Subject Alternate Names to consider
  as valid.
* Items in this list are never validated against the SSL Common Name.
* This feature does not work with the deployment server and client
  communication over SSL.
* Optional.  
* Default: No alternate name checking.

requireClientCert = <boolean>
* Requires that any HTTPS client that connects to a splunkd 
  internal HTTPS server has a certificate that was signed by a 
  CA (Certificate Authority) specified by the 'sslRootCAPath' setting.
  * Used by distributed search: Splunk indexing instances must be
  authenticated to connect to another splunk indexing instance.
  * Used by distributed deployment: The deployment server requires that
  deployment clients are authenticated before allowing them to poll for new
  configurations/applications.
* If set to "true", a client can connect ONLY if a certificate 
  created by our certificate authority was used on that client.
* Default: false

cipherSuite = <cipher suite string>
* If set, Splunk uses the specified cipher string for the HTTP server.
* If not set, Splunk uses the default cipher string provided by OpenSSL.
  This is used to ensure that the server does not accept connections using
  weak encryption protocols.
* Must specify 'dhFile' to enable any Diffie-Hellman ciphers.
* Default: The default can vary. See the 'cipherSuite' setting in
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

ecdhCurveName = <string>
* DEPRECATED.
* Use the 'ecdhCurves' setting instead.
* This setting specifies the Elliptic Curve Diffie-Hellman (ECDH) curve to
  use for ECDH key negotiation.
* Splunk only supports named curves that have been specified by their 
  SHORT name.
* The list of valid named curves by their short and long names
  can be obtained by running this CLI command:
  $SPLUNK_HOME/bin/splunk cmd openssl ecparam -list_curves
* Default: empty string.

ecdhCurves = <comma-separated list>
* A list of ECDH curves to use for ECDH key negotiation.
* The curves should be specified in the order of preference.
* The client sends these curves as a part of an SSL Client Hello.
* The server supports only the curves specified in the list.
* Splunk software only supports named curves that have been specified
  by their SHORT names.
* The list of valid named curves by their short and long names can be obtained
  by running this CLI command:
  $SPLUNK_HOME/bin/splunk cmd openssl ecparam -list_curves
* Example setting: "ecdhCurves = prime256v1,secp384r1,secp521r1"
* The default can vary. See the 'ecdhCurves' setting in
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

serverCert = <path>
* The full path to the PEM (Privacy-Enhanced Mail) format server 
  certificate file.
* Certificates are auto-generated by splunkd upon starting Splunk.
* You can replace the default certificate with your own PEM 
  format file.
* Default: $SPLUNK_HOME/etc/auth/server.pem

sslKeysfile = <filename>
* DEPRECATED. Use the 'serverCert' setting instead.
* This file is in the directory specified by the 'caPath' setting 
  (see below).
* Default: server.pem

sslPassword = <password>
* Server certificate password.
* Default: "password"

sslKeysfilePassword = <password>
* DEPRECATED. Use the 'sslPassword' setting instead.

sslRootCAPath = <path>
* Full path to the root CA (Certificate Authority) certificate store
  on the operating system.
* The <path> must refer to a PEM (Privacy-Enhanced Mail) format 
  file containing one or more root CA certificates concatenated 
  together.
* Required for Common Criteria.
* This setting is valid on Windows machines only if you have not set
  'sslRootCAPathHonoredOnWindows' to "false".
* No default.

sslRootCAPathHonoredOnWindows = <boolean>
* DEPRECATED.
* Whether or not the Splunk instance respects the 'sslRootCAPath' setting on
  Windows machines.
* If you set this setting to "false", then the instance does not respect the
  'sslRootCAPath' setting on Windows machines.
* This setting is valid only on Windows, and only if you have set
  'sslRootCAPath'.
* When the 'sslRootCAPath' setting is respected, the instance expects to find
  a valid PEM file with valid root certificates that are referenced by that
  path. If a valid file is not present, SSL communication fails.
* Default: true.

caCertFile = <filename>
* DEPRECATED. Use the 'sslRootCAPath' setting instead.
* Used only if 'sslRootCAPath' is not set.
* File name (relative to 'caPath') of the CA (Certificate Authority)
  certificate PEM format file containing one or more certificates 
  concatenated together.
* Default: cacert.pem

dhFile = <path>
* PEM (Privacy-Enhanced Mail) format Diffie-Hellman(DH) parameter file name.
* DH group size should be no less than 2048bits.
* This file is required in order to enable any Diffie-Hellman ciphers.
* No default.

caPath = <path>
* DEPRECATED. Use absolute paths for all certificate files.
* If certificate files given by other settings in this stanza are not absolute
  paths, then they are relative to this path.
* Default: $SPLUNK_HOME/etc/auth.

certCreateScript = <script name>
* Creation script for generating certificates on startup of Splunk.

sendStrictTransportSecurityHeader = <boolean>
* If set to "true", the REST interface sends a "Strict-Transport-Security"
  header with all responses to requests made over SSL.
* This can help avoid a client being tricked later by a 
  Man-In-The-Middle attack to accept a non-SSL request.  
  However, this requires a commitment that no non-SSL web hosts 
  ever run on this hostname on any port. For
  example, if splunkweb is in default non-SSL mode this can break the
  ability of a browser to connect to it.  
* NOTE: Enable with caution.
* Default: false

allowSslCompression = <boolean>
* If set to "true", the server allows clients to negotiate
  SSL-layer data compression.
* KV Store also observes this setting. 
* If set to "false", KV Store disables TLS compression.
* Default: true

allowSslRenegotiation = <boolean>
* In the SSL protocol, a client may request renegotiation of the 
  connection settings from time to time.
* If set to "false", causes the server to reject all renegotiation
  attempts, breaking the connection.  This limits the amount of CPU a
  single TCP connection can use, but it can cause connectivity problems
  especially for long-lived connections.
* Default: true

sslClientSessionPath = <path>
* Path where all client sessions are stored for session re-use.
* Used if 'useSslClientSessionCache' is set to "true".
* No default.

useSslClientSessionCache = <boolean>
* Specifies whether to re-use client session.
* When set to "true", client sessions are stored in memory for 
  session re-use. This reduces handshake time, latency and 
  computation time to improve SSL performance.
* When set to "false", each SSL connection performs a full 
  SSL handshake.
* Default: false

sslServerSessionTimeout = <integer>
* Timeout, in seconds, for newly created session.
* If set to "0", disables Server side session cache.
* The openssl default is 300 seconds.
* Default: 300 (5 minutes)

sslServerHandshakeTimeout = <integer>
* The timeout, in seconds, for an SSL handshake to complete between an
  SSL client and the Splunk SSL server.
* If the SSL server does not receive a "Client Hello" from the SSL client within
  'sslServerHandshakeTimeout' seconds, the server terminates
  the connection.
* Default: 60


#############################################################################
# Splunkd http proxy configuration
#############################################################################
[proxyConfig]
http_proxy = <string>
* If set, splunkd sends all HTTP requests through the proxy server 
  that you specify.
* No default.

https_proxy = <string>
* If set, splunkd sends all HTTPS requests through the proxy server 
  that you specify. 
* If not set, splunkd uses the 'http_proxy' setting instead.
* No default.

no_proxy = <string>
* If set, splunkd uses the no_proxy rules to decide whether the proxy 
  server needs to be bypassed for matching hosts/IP Addresses. 
  Requests going to localhost/loopback address are not proxied.
* '*' (asterisk): Bypasses proxies for all requests. This is the only 
  wildcard, and it can be used only by itself.
* <IPv4 or IPv6 address>: Bypasses the proxy if the request is intended for
  that IP address.
* <hostname>/<domain name>: Bypasses the proxy if the request is intended for
  that host or domain name. For example:
  * no_proxy = "wimpy"   This matches the host name "wimpy"
  * no_proxy = "splunk.com"   This matches all host names in the splunk.com
    domain (apps.splunk.com, www.splunk.com, and so on.)
* If any of the rules in the list has a '*', then that rule overrides all
  other rules, and proxies are bypassed for all requests.
* Default: localhost, 127.0.0.1, ::1

############################################################################
# Splunkd HTTP server configuration
############################################################################

[httpServer]
* Set stand-alone HTTP settings for splunkd under this stanza name.
* Follow this stanza name with any number of the following attribute/value
  pairs.
* If you do not specify an entry for each attribute, splunkd uses the default
  value.

atomFeedStylesheet = <string>
* Defines the stylesheet relative URL to apply to default Atom feeds.
* Set to 'none' to stop writing out xsl-stylesheet directive.
* Default: /static/atom.xsl

max-age = <nonnegative integer>
* Set the maximum time, in seconds, to cache a static asset served off of
  the '/static' directory.
* This value is passed along in the 'Cache-Control' HTTP header.
* Default: 3600 (60 minutes)

follow-symlinks = <boolean>
* Specifies whether the static file handler (serving the '/static' 
  directory) follows filesystem symlinks when serving files.
* Default: false

disableDefaultPort = <boolean>
* If set to "true", turns off listening on the splunkd management port,
  which is 8089 by default.
* NOTE: Changing this setting is not recommended.
  * This is the general communication path to splunkd.  If it is disabled,
    there is no way to communicate with a running splunk.
  * This means many command line splunk invocations cannot function,
    splunkweb cannot function, the REST interface cannot function, etc.
  * If you choose to disable the port anyway, understand that you are
    selecting reduced Splunk functionality.
* Default: false

acceptFrom = <network_acl> ...
* Lists a set of networks or addresses from which to accept connections.
* This setting only takes effect when 'appServerPorts' is set to a
  non-zero value.
* Separate multiple rules with commas or spaces.
* Each rule can be in one of the following formats:
    1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    2. A Classless Inter-Domain Routing (CIDR) block of addresses
       (examples: "10/8", "192.168.1/24", "fe80:1234/32")
    3. A DNS name, possibly with a "*" used as a wildcard
       (examples: "myhost.example.com", "*.splunk.com")
    4. "*", which matches anything
* You can also prefix an entry with '!' to cause the rule to reject the
  connection. The input applies rules in order, and uses the first one that
  matches.
  For example, "!10.1/16, *" allows connections from everywhere except
  the 10.1.*.* network.
* Default: "*" (accept from anywhere)

streamInWriteTimeout = <positive number>
* The timeout, in seconds, for uploading data to the http server.
* When uploading data to http server, if the http server is unable 
  to write data to the receiver for the specified value, the operation
  aborts.
* Default: 5

max_content_length = <integer>
* Maximum content length, in bytes.
* HTTP requests over the size specified are rejected.
* This setting exists to avoid allocating an unreasonable amount 
  of memory from web requests.
* In environments where indexers have enormous amounts of RAM, this
  number can be reasonably increased to handle large quantities of
  bundle data.
* Default: 2147483648 (2GB)

maxSockets = <integer>
* The number of simultaneous HTTP connections that Splunk Enterprise accepts
  simultaneously. You can limit this number to constrain resource usage.
* If set to "0", Splunk Enterprise automatically sets maxSockets to 
  one third of the maximum allowable open files on the host.
* If this number is less than 50, it is set to 50. 
* If this number is greater than 400000, it is set to 400000.
* If set to a negative number, no limit is enforced.
* Default: 0

maxThreads = <integer>
* The number of threads that can be used by active HTTP transactions.
  You can limit this number to constrain resource usage.
* If set to 0, Splunk Enterprise automatically sets the limit to
  one third of the maximum allowable threads on the host.
* If this number is less than 20, it is set to 20. If this number is
  greater than 150000, it is set to 150000.
* If maxSockets is not negative and maxThreads is greater than maxSockets, then
  Splunk Enterprise sets maxThreads to be equal to maxSockets.
* If set to a negative number, no limit is enforced.
* Default: 0

keepAliveIdleTimeout = <integer>
* How long, in seconds, that the Splunkd HTTP server allows a keep-alive
  connection to remain idle before forcibly disconnecting it.
* If this number is less than 7200, it is set to 7200.
* Default: 7200 (12 minutes)

busyKeepAliveIdleTimeout = <integer>
* How long, in seconds, that the Splunkd HTTP server allows a keep-alive
  connection to remain idle while in a busy state before forcibly disconnecting it.
* Use caution when configuring this setting as a value that is too large
  can result in file descriptor exhaustion due to idling connections.
* If this number is less than 12, it is set to 12.
* Default: 12

forceHttp10 = auto|never|always
* When set to "always", the REST HTTP server does not use some
  HTTP 1.1 features such as persistent connections or chunked
  transfer encoding.
* When set to "auto" it does this only if the client sent no
  User-Agent header, or if the user agent is known to have bugs
  in its HTTP/1.1 support.
* When set to "never" it always allows HTTP 1.1, even to
  clients it suspects may be buggy.
* Default: "auto"

crossOriginSharingPolicy = <origin_acl> ...
* List of the HTTP Origins for which to return Access-Control-Allow-* (CORS)
  headers.
* These headers tell browsers that we trust web applications at those sites
  to make requests to the REST interface
* The origin is passed as a URL without a path component (for example
  "https://app.example.com:8000")
* This setting can take a list of acceptable origins, separated
  by spaces and/or commas
* Each origin can also contain wildcards for any part.  Examples:
    *://app.example.com:*  (either HTTP or HTTPS on any port)
    https://*.example.com  (any host under example.com, including example.com itself)
* An address can be prefixed with a '!' to negate the match, with
  the first matching origin taking precedence.  For example,
  "!*://evil.example.com:* *://*.example.com:*" to not avoid
  matching one host in a domain
* A single "*" can also be used to match all origins
* No default.

x_frame_options_sameorigin = <boolean>
* Adds a X-Frame-Options header set to "SAMEORIGIN" to every response served by splunkd
* Default: true

allowEmbedTokenAuth = <boolean>
* If set to false, splunkd does not allow any access to artifacts
  that previously had been explicitly shared to anonymous users.
* This effectively disables all use of the "embed" feature.
* Default: true

cliLoginBanner = <string>
* Sets a message which is added to the HTTP reply headers
  of requests for authentication, and to the "server/info" endpoint
* This is printed by the Splunk CLI before it prompts
  for authentication credentials.  This can be used to print
  access policy information.
* If this string starts with a '"' character, it is treated as a
  CSV-style list with each line comprising a line of the message.
  For example: "Line 1","Line 2","Line 3"
* No default.

allowBasicAuth = <boolean>
* Allows clients to make authenticated requests to the splunk
  server using "HTTP Basic" authentication in addition to the
  normal "authtoken" system
* This is useful for programmatic access to REST endpoints and
  for accessing the REST API from a web browser.  It is not
  required for the UI or CLI.
* Default: true

basicAuthRealm = <string>
* When using "HTTP Basic" authenitcation, the 'realm' is a
  human-readable string describing the server.  Typically, a web
  browser presents this string as part of its dialog box when
  asking for the username and password.
* This can be used to display a short message describing the
  server and/or its access policy.
* Default: "/splunk"

allowCookieAuth = <boolean>
* Allows clients to request an HTTP cookie from the /services/auth/login
  endpoint which can then be used to authenticate future requests
* Default: true

cookieAuthHttpOnly = <boolean>
* When using cookie based authentication, mark returned cookies
  with the "httponly" flag to tell the client not to allow javascript
  code to access its value
* NOTE: has no effect if allowCookieAuth=false
* Default: true

cookieAuthSecure = <boolean>
* When using cookie based authentication, mark returned cookies
  with the "secure" flag to tell the client never to send it over
  an unencrypted HTTP channel
* NOTE: has no effect if allowCookieAuth=false OR the splunkd REST
  interface has SSL disabled
* Default: true

dedicatedIoThreads = <integer>
* If set to zero, HTTP I/O is performed in the same thread
  that accepted the TCP connection.
* If set set to a non-zero value, separate threads are run
  to handle the HTTP I/O, including SSL encryption.
* Typically this setting does not need to be changed.  For most usage
  scenarios using the same the thread offers the best performance.
* Default: 0

replyHeader.<name> = <string>
* Add a static header to all HTTP responses this server generates
* For example, "replyHeader.My-Header = value" causes the
  response header "My-Header: value" to be included in the reply to
  every HTTP request to the REST server

############################################################################
# Splunkd HTTPServer listener configuration
############################################################################

[httpServerListener:<ip:><port>]
* Enable the splunkd REST HTTP server to listen on an additional port number
  specified by <port>.  If a non-empty <ip> is included (for example:
  "[httpServerListener:127.0.0.1:8090]") the listening port is
  bound only to a specific interface.
* Multiple "httpServerListener" stanzas can be specified to listen on
  more ports.
* Normally, splunkd listens only on the single REST port specified in
  the web.conf "mgmtHostPort" setting, and none of these stanzas need to
  be present. Add these stanzas only if you want the REST HTTP server
  to listen to more than one port.

ssl = <boolean>
* Toggle whether this listening ip:port uses SSL or not.
* If the main REST port is SSL (the "enableSplunkdSSL" setting in this
  file's [sslConfig] stanza) and this stanza is set to "ssl=false" then
  clients on the local machine such as the CLI may connect to this port.
* Default: true

listenOnIPv6 = no|yes|only
* Toggle whether this listening ip:port listens on IPv4, IPv6, or both.
* If not present, the setting in the [general] stanza is used

acceptFrom = <network_acl> ...
* Lists a set of networks or addresses from which to accept connections.
* This setting only takes effect when 'appServerPorts' is set to a
  non-zero value.
* Separate multiple rules with commas or spaces.
* Each rule can be in one of the following formats:
    1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    2. A Classless Inter-Domain Routing (CIDR) block of addresses
       (examples: "10/8", "192.168.1/24", "fe80:1234/32")
    3. A DNS name, possibly with a "*" used as a wildcard
       (examples: "myhost.example.com", "*.splunk.com")
    4. "*", which matches anything
* You can also prefix an entry with '!' to cause the rule to reject the
  connection. The input applies rules in order, and uses the first one that
  matches.
  For example, "!10.1/16, *" allows connections from everywhere except
  the 10.1.*.* network.
* Default: The setting in the [httpServer] stanza

############################################################################
# Static file handler MIME-type map
############################################################################

[mimetype-extension-map]
* Map filename extensions to MIME type for files served from the static file
  handler under this stanza name.

<file-extension> = <MIME-type>
* Instructs the HTTP static file server to mark any files ending
  in 'file-extension' with a header of 'Content-Type: <MIME-type>'.
* Default:
    [mimetype-extension-map]
    gif = image/gif
    htm = text/html
    jpg = image/jpg
    png = image/png
    txt = text/plain
    xml = text/xml
    xsl = text/xml

############################################################################
# Log rotation of splunkd_stderr.log & splunkd_stdout.log
############################################################################

# These stanzas apply only on UNIX.  splunkd on Windows has no
# stdout.log or stderr.log files.

[stderr_log_rotation]
* Controls the data retention of the file containing all messages written to
  splunkd's stderr file descriptor (fd 2).
* Typically this is extremely small, or mostly errors and warnings from
  linked libraries.

maxFileSize = <bytes>
* When splunkd_stderr.log grows larger than this value, it is rotated.
* maxFileSize is expressed in bytes.
* You might want to increase this if you are working on a problem
  that involves large amounts of output to the splunkd_stderr.log file.
* You might want to reduce this to allocate less storage to this log category.
* Default: 10000000 (10 si-megabytes)

BackupIndex = <non-negative integer>
* How many rolled copies to keep.
* For example, if this setting is 2, the splunkd_stderr.log.1 and 
  splunkd_stderr.log.2 file might exist. Further rolls delete the 
  current splunkd_stderr.log.2 file.
* You might want to increase this value if you are working on a problem
  that involves large amounts of output to the splunkd_stderr.log fils
* You might want to reduce this to allocate less storage to this log category.
* Default: 2

checkFrequency = <seconds>
* How often. in seconds, to check the size of splunkd_stderr.log
* Larger values may result in larger rolled file sizes but take less resources.
* Smaller values may take more resources but more accurately constrain the
  file size.
* Default: 10

[stdout_log_rotation]
* Controls the data retention of the file containing all messages written to
  splunkd's stdout file descriptor (fd 1).
* Almost always, there is nothing in this file.

* This stanza can have the same settings as the [stderr_log_rotation]
  stanza with the same defaults.  See above for definitions.

maxFileSize = <bytes>
BackupIndex = <non-negative integer>
checkFrequency = <seconds>

############################################################################
# Remote applications configuration (e.g. SplunkBase)
############################################################################

[applicationsManagement]
* Set remote applications settings for Splunk under this stanza name.
* Follow this stanza name with any number of the following attribute/value
  pairs.
* If you do not specify an entry for each attribute, Splunk uses the default
  value.

allowInternetAccess = <boolean>
* Allow Splunk to access the remote applications repository.

url = <URL>
* Applications repository.
* Default: https://apps.splunk.com/api/apps

loginUrl = <URL>
* Applications repository login.
* Default: https://apps.splunk.com/api/account:login/

detailsUrl = <URL>
* Base URL for application information, keyed off of app ID.
* Default: https://apps.splunk.com/apps/id

useragent = <splunk-version>-<splunk-build-num>-<platform>
* User-agent string to use when contacting applications repository.
* <platform> includes information like operating system and CPU architecture.

updateHost = <URL>
* Host section of URL to check for app updates, e.g. https://apps.splunk.com

updatePath = <URL>
* Path section of URL to check for app updates
  For example: /api/apps:resolve/checkforupgrade

updateTimeout = <time range string>
* The minimum amount of time Splunk software waits between checks for
  app updates.
* Examples include '24h' (24 hours), '3d' (3 days),
  '7200s' (7200 seconds, or two hours)
* Default: 24h

sslVersions = <versions_list>
* Comma-separated list of SSL versions to connect to 'url' (https://apps.splunk.com).
* The versions available are "ssl3", "tls1.0", "tls1.1", and "tls1.2".
* The special version "*" selects all supported versions.  The version "tls"
  selects all versions tls1.0 or newer.
* If a version is prefixed with "-" it is removed from the list.
* SSLv2 is always disabled; "-ssl2" is accepted in the version list but does nothing.
* When configured in FIPS mode, ssl3 is always disabled regardless
  of this configuration.
* Default: The default can vary. See the 'sslVersions' setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

sslVerifyServerCert = <boolean>
* If this is set to true, Splunk verifies that the remote server (
  specified in 'url') being connected to is a valid one (authenticated).  
  Both the common name and the alternate name of the server are then 
  checked for a match if they are specified in 'sslCommonNameToCheck' and 
  'sslAltNameToCheck'. A certificate is considered verified if either 
  is matched.
* Default: true

caCertFile = <path>
* Full path to a CA (Certificate Authority) certificate(s) PEM format file.
* The <path> must refer to a PEM format file containing one or more root CA
  certificates concatenated together.
* Used only if 'sslRootCAPath' is not set.
* Used for validating SSL certificate from https://apps.splunk.com/

sslCommonNameToCheck = <commonName1>, <commonName2>, ...
* If this value is set, and 'sslVerifyServerCert' is set to true,
  splunkd checks the common name(s) of the certificate presented by
  the remote server (specified in 'url') against this list of common names.
* Default: apps.splunk.com

sslCommonNameList = <commonName1>, <commonName2>, ...
* DEPRECATED. Use the 'sslCommonNameToCheck' setting instead.

sslAltNameToCheck =  <alternateName1>, <alternateName2>, ...
* If this value is set, and 'sslVerifyServerCert' is set to true,
  splunkd checks the alternate name(s) of the certificate presented by
  the remote server (specified in 'url') against this list of subject 
  alternate names.
* Default: splunkbase.splunk.com, apps.splunk.com

cipherSuite = <cipher suite string>
* Uses the specified cipher string for making outbound HTTPS connection.
* Default: The default can vary. See the 'cipherSuite' setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the current default.

ecdhCurves = <comma separated list of ec curves>
* ECDH curves to use for ECDH key negotiation.
* The curves should be specified in the order of preference.
* The client sends these curves as a part of Client Hello.
* We only support named curves specified by their SHORT names.
  (see struct ASN1_OBJECT in asn1.h)
* The list of valid named curves by their short/long names can be obtained
  by executing this command:
  $SPLUNK_HOME/bin/splunk cmd openssl ecparam -list_curves
* e.g. ecdhCurves = prime256v1,secp384r1,secp521r1
* Default: The default can vary. See the 'ecdhCurves' setting in
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

############################################################################
# Misc. configuration
############################################################################

[scripts]

initialNumberOfScriptProcesses = <num>
* The number of pre-forked script processes that are launched when the
  system comes up. These scripts are reused when script REST endpoints
  *and* search scripts are executed.
  The idea is to eliminate the performance overhead of launching the script
  interpreter every time it is invoked.  These processes are put in a pool.
  If the pool is completely busy when a script gets invoked, a new processes
  is fired up to handle the new invocation - but it disappears when that
  invocation is finished.


############################################################################
# Disk usage settings (for the indexer, not for Splunk log files)
############################################################################

[diskUsage]

minFreeSpace = <num>|<percentage>
* Minimum free space for a partition.
* Specified as an integer that represents a size in binary
  megabytes (ie MiB) or as a percentage, written as a decimal
  between 0 and 100 followed by a '%' sign, for example "10%"
  or "10.5%"
* If specified as a percentage, this is taken to be a percentage of
  the size of the partition. Therefore, the absolute free space required
  varies for each partition depending on the size of that partition.
* Specifies a safe amount of space that must exist for splunkd to continue
  operating.
* Note that this affects search and indexing
* For search:
  * Before attempting to launch a search, Splunk software requires this
    amount of free space on the filesystem where the dispatch directory 
    is stored, $SPLUNK_HOME/var/run/splunk/dispatch
  * Applied similarly to the search quota values in authorize.conf and
    limits.conf.
* For indexing:
  * Periodically, the indexer checks space on all partitions
    that contain splunk indexes as specified by indexes.conf. Indexing
    is paused and a ui banner + splunkd warning posted to indicate
    need to clear more disk space.
* Default: 5000 (approx 5GB)

pollingFrequency = <num>
* Specifies that after every 'pollingFrequency' events are indexed, 
  the disk usage is checked.
* Default: 100000

pollingTimerFrequency = <num>
* Minimum time, in seconds, between two disk usage checks.
* Default: 10

############################################################################
# Queue settings
############################################################################
[queue]

maxSize = [<integer>|<integer>[KB|MB|GB]]
* Specifies default capacity of a queue.
* If specified as a lone integer (for example, maxSize=1000), maxSize
  indicates the maximum number of events allowed in the queue.
* If specified as an integer followed by KB, MB, or GB (for example,
  maxSize=100MB), it indicates the maximum RAM allocated for queue.
* Default: 500KB

cntr_1_lookback_time = [<integer>[s|m]]
* The lookback counters are used to track the size and count (number of
  elements in the queue) variation of the queues using an exponentially
  moving weighted average technique. Both size and count variation
  has 3 sets of counters each. The set of 3 counters is provided to be able
  to track short, medium and long term history of size/count variation. The
  user can customize the value of these counters or lookback time.
* Specifies how far into history should the size/count variation be tracked
  for counter 1.
* It must be an integer followed by [s|m] which stands for seconds and
  minutes respectively.
* Default: 60s

cntr_2_lookback_time = [<integer>[s|m]]
* See above for explanation and usage of the lookback counter.
* Specifies how far into history should the size/count variation be tracked
  for counter 2.
* Default: 600s (10 minutes)

cntr_3_lookback_time = [<integer>[s|m]]
* See above for explanation and usage of the lookback counter..
* Specifies how far into history should the size/count variation be tracked
  for counter 3.
* Default: 900s (15 minutes).

sampling_interval = [<integer>[s|m]]
* The lookback counters described above collects the size and count
  measurements for the queues. This specifies at what interval the
  measurement collection happens. Note that for a particular queue all
  the counters sampling interval is same.
* It needs to be specified via an integer followed by [s|m] which stands for
  seconds and minutes respectively.
* Default: 1s

[queue=<queueName>]

maxSize = [<integer>|<integer>[KB|MB|GB]]
* Specifies the capacity of a queue. It overrides the default capacity
  specified in the [queue] stanza.
* If specified as a lone integer (for example, maxSize=1000), maxSize
  indicates the maximum number of events allowed in the queue.
* If specified as an integer followed by KB, MB, or GB (for example,
  maxSize=100MB), it indicates the maximum RAM allocated for queue.
* Default: The default is inherited from the 'maxSize' value specified 
  in the [queue] stanza.

cntr_1_lookback_time = [<integer>[s|m]]
* Same explanation as mentioned in the [queue] stanza.
* Specifies the lookback time for the specific queue for counter 1.
* Default: The default value is inherited from the 'cntr_1_lookback_time'
  value that is specified in the [queue] stanza.

cntr_2_lookback_time = [<integer>[s|m]]
* Specifies the lookback time for the specific queue for counter 2.
* Default: The default value is inherited from the 'cntr_2_lookback_time' 
  value that is specified in the [queue] stanza.

cntr_3_lookback_time = [<integer>[s|m]]
* Specifies the lookback time for the specific queue for counter 3.
* Default: The default value is inherited from the 'cntr_3_lookback_time' value 
  that is specified in the [queue] stanza.

sampling_interval = [<integer>[s|m]]
* Specifies the sampling interval for the specific queue.
* Default: The default value is inherited from the 'sampling_interval' value 
  specified in the [queue] stanza.

############################################################################
# PubSub server settings for the http endpoint.
############################################################################

[pubsubsvr-http]

disabled = <boolean>
* If disabled, then http endpoint is not registered. Set this value to
  'false' to expose PubSub server on http.
* Default: true

stateIntervalInSecs = <seconds>
* The number of seconds before a connection is flushed due to inactivity.
  The connection is not closed, only messages for that connection are
  flushed.
* Default: 300 (5 minutes)

############################################################################
# General file input settings. ** NOT SUPPORTED **
############################################################################

# [fileInput]
# outputQueue = <queue name>
* REMOVED. Historically this allowed the user to set the target queue for the
  file-input (tailing) processor, but there was no valid reason to modify this.
* This setting is now removed, and has no effect.
* Tailing always uses the parsingQueue.

############################################################################
# Settings controlling the behavior of 'splunk diag', the diagnostic tool
############################################################################

[diag]

# These settings provide defaults for invocations of the splunk diag
# command. Generally these can be further modified by command line flags to
# the diag command.

EXCLUDE-<class> = <glob expression>
* Specifies a glob / shell pattern to be excluded from diags generated on
  this Splunk instance.
  * Example: */etc/secret_app/local/*.conf
* Further excludes can be added at the splunk diag command line, but there
  is no facility to disable configuration-based excludes at the command
  line.
* There is one exclude by default, for the splunk.secret file.

# the following commands can be overridden entirely by their command-line
# equivalents.

components = <comma separated list>
* Specifies which components of the diag should be gathered.
* This allows the disabling and enabling, categorically, of entire portions
  of diag functionality.
* All of these components are further subject to the exclude feature (see
  above), and component-specific filters (see below).
* Currently, with no configuration, all components except "rest" are enabled
  by default.
* Available components are:
  * index_files   : Files from the index that indicate their health
                    (Hosts|Sources|Sourcetypes.data and bucketManifests).
                    User data is not collected.
  * index_listing : Directory listings of the index contents are
                    gathered, in order to see filenames, directory names,
                    sizes, timestamps and the like.
  * etc           : The entire contents of the $SPLUNK_HOME/etc
                    directory.  In other words, the configuration files.
  * log           : The contents of $SPLUNK_HOME/var/log/...
  * pool          : If search head pooling is enabled, the contents of the
                    pool dir.
  * dispatch      : Search artifacts, without the actual results,
                    In other words var/run/splunk/dispatch, but not the
                    results or events files
  * searchpeers   : Directory listings of knowledge bundles replicated for
                    distributed search
                    In other words: $SPLUNK_HOME/var/run/searchpeers
  * consensus     : Consensus protocol files produced by search head clustering
                    In other words: $SPLUNK_HOME/var/run/splunk/_raft
  * conf_replication_summary : Directory listing of configuration
                    replication summaries produced by search head clustering
                    In other words: $SPLUNK_HOME/var/run/splunk/snapshot
  * rest          : The contents of a variety of splunkd endpoints
                    Includes server status messages (system banners),
                    licenser banners, configured monitor inputs & tailing
                    file status (progress reading input files).
                    * On cluster masters, also gathers master info, fixups,
                      current peer list, clustered index info, current
                      generation, & buckets in bad stats
                    * On cluster slaves, also gathers local buckets & local
                      slave info, and the master information remotely from
                      the configured master.
  * kvstore       : Directory listings of the KV Store data directory
                    contents are gathered, in order to see filenames,
                    directory names, sizes, and timestamps.
  * file_validate : Produce list of files that were in the install media
                    which have been changed.  Generally this should be an
                    empty list.

* The special value "all" is also supported, enabling everything explicitly.
* Further controlling the components from the command line:
    * The switch --collect replaces this list entirely.
        * Example: --collect log,etc
          This would set the components to log and etc only, regardless of
           onfig
    * The switch --enable adds a specific component to this list.
        * Example: --enable pool
          This would ensure that pool data is collected, regardless of
          config
    * The switch --disable removes a specific component from this list.
        * Example: --disable pool
          This would ensure that pool data is *NOT* collected, regardless of
          config
* Default: To collect all components, except "rest".

# Data filters; these further refine what is collected
# most of the existing ones are designed to limit the size and collection
# time to pleasant values.

# NOTE: Most values here use underscores '_' while the command line uses
# hyphens '-'

all_dumps = <boolean>
* This setting currently is irrelevant on UNIX platforms.
* Affects the 'log' component of diag. (dumps are written to the log dir
  on Windows)
* Can be overridden with the --all-dumps command line flag.
* Normally, Splunk diag gathers only three .DMP (crash dump) files on
  Windows to limit diag size.
* If this is set to true, splunk diag collects *all* .DMP files from
  the log directory.
* No default. (false equivalent).

index_files = [full|manifests]
* Selects a detail level for the 'index_files' component.
* Can be overridden with the --index-files command line flag.
* If set to 'manifests', limits the index file-content collection to just
  .bucketManifest files which give some information about the general state of
  buckets in an index.
* If set to 'full', adds the collection of Hosts.data, Sources.data, and
  Sourcetypes.data which indicate the breakdown of count of items by those
  categories per-bucket, and the timespans of those category entries
    * 'full' can take quite some time on very large index sizes, especially
      when slower remote storage is involved.
* Default: manifests

index_listing = [full|light]
* Selects a detail level for the 'index_listing' component.
* Can be overridden with the --index-listing command line flag.
* 'light' gets directory listings (ls, or dir) of the hot/warm and cold
  container directory locations of the indexes, as well as listings of each
  hot bucket.
* 'full' gets a recursive directory listing of all the contents of every
  index location, which should mean all contents of all buckets.
  * 'full' may take significant time as well with very large bucket counts,
    especially on slower storage.
* Default: light

etc_filesize_limit = <non-negative integer in kilobytes>
* This filters the 'etc' component
* Can be overridden with the --etc-filesize-limit command line flag
* This value is specified in kilobytes.
    * Example: 2000 - this would be approximately 2MB.
* Files in the $SPLUNK_HOME/etc directory which are larger than this limit
  is not collected in the diag.
* Diag produces a message stating that a file has been skipped for size
  to the console. (In practice we found these large files are often a
  surprise to the administrator and indicate problems).
* If desired, this filter may be entirely disabled by setting the value
  to 0.
* Currently, as a special exception, the file 
  $SPLUNK_HOME?etc/system/replication/ops.json is permitted to be 10x the
  size of this limit.
* Default: 10000 (10MB)

log_age = <non-negative integer in days>
* This filters the 'log' component
* Can be overridden with the --log-age command line flag
* This value is specified in days
  * Example: 75 - this would be 75 days, or about 2.5 months.
* If desired, this filter may be entirely disabled by setting the value to 0.
* The idea of this default filter is that data older than this is rarely
  helpful in troubleshooting cases in any event.
* Default: 60 (or approximately 2 months)

upload_proto_host_port = <protocol://host:port>|disabled
* URI base to use for uploading files/diags to Splunk support.
* If set to disabled (override in a local/server.conf file), effectively
  disables diag upload functionality for this Splunk install.
* Modification may theoretically may permit operations with some forms of
  proxies, but diag is not specifically designed for such, and support of proxy
  configurations that do not currently work is considered an Enhancement
  Request.
* The communication path with api.splunk.com is over a simple but not
  documented protocol.  If for some reason you wish to accept diag uploads into
  your own systems, it probably is simpler to run diag and then upload via
  your own means independently.  However if you have business reasons that you
  want this built-in, get in touch.
* Uploading to unencrypted http definitely not recommended.
* Default: https://api.splunk.com

SEARCHFILTERSIMPLE-<class> = regex
SEARCHFILTERLUHN-<class> = regex
* Redacts strings from ad-hoc searches logged in the audit.log and 
  remote_searches.log files.
* Substrings which match these regexes *inside* a search string in one of those
  two files is replaced by sequences of the character X, as in XXXXXXXX.
* Substrings which match a SEARCHFILTERLUHN regex has the contained
  numbers further tested against the luhn algorithm, used for data integrity
  in mostly financial circles, such as credit card numbers.  This permits more
  accurate identification of that type of data, relying less heavily on regex
  precision. See the Wikipedia article on the "Luhn algorithm" for additional
  information.
* Search string filtering is entirely disabled if --no-filter-searchstrings is
  used on the command line.
* NOTE: That matching regexes must take care to match only the bytes of the
  term.  Each match "consumes" a portion of the search string, so matches that
  extend beyond the term (for example, to adjacent whitespace) could prevent
  subsequent matches, and/or redact data needed for troubleshooting.
* Please use a name hinting at the purpose of the filter in the <class>
  component of the setting name, and consider an additional explicative
  comment, even for custom local settings. This might skip inquiries from
  support.

############################################################################
# Application License manager settings for configuring app license checking
############################################################################

[applicense]
appLicenseHostPort = <IP:port>
* Specifies the location of the IP address or DNS name and port of the app
  license server.

appLicenseServerPath = <path>
* Specifies the path portion of the URI of the app license server.

caCertFile = <path>
* Full path to a CA (Certificate Authority) certificate(s) PEM format file.
* NOTE: Splunk plans to submit Splunk Enterprise for Common Criteria
  evaluation. Splunk does not support using the product in Common
  Criteria mode until it has been certified by NIAP. See the "Securing
  Splunk Enterprise" manual for information on the status of Common
  Criteria certification.
* Default: $SPLUNK_HOME/etc/auth/cacert.pem

sslVersions = <versions_list>
* Comma-separated list of SSL versions to support.
* The special version "*" selects all supported versions.  The version "tls"
  selects all versions tls1.0 or newer.
* If a version is prefixed with "-" it is removed from the list.
* SSLv2 is always disabled; "-ssl2" is accepted in the version list but does nothing.
* When configured in FIPS mode, ssl3 is always disabled regardless
  of this configuration.
* Default: The default can vary. See the 'sslVersions' setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

cipherSuite = <cipher suite string>
* If set, uses the specified cipher string for the SSL connection.
* Default: The default can vary. See the 'cipherSuite' setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the 
  current default.

sslVerifyServerCert = <boolean>
* If this is set to true, Splunk verifies that the remote server (specified in 'url')
  being connected to is a valid one (authenticated).  Both the common
  name and the alternate name of the server are then checked for a
  match if they are specified in 'sslCommonNameToCheck' and 'sslAltNameToCheck'.
  A certificate is considered verified if either is matched.
* Default: true

sslCommonNameToCheck = <commonName1>, <commonName2>, ...
* If this value is set, and 'sslVerifyServerCert' is set to true,
  splunkd limits most outbound HTTPS connections to hosts which use
  a cert with one of the listed common names.
* Default:  Some common name checking
.
sslAltNameToCheck = <alternateName1>, <alternateName2>, ...
* If this value is set, and 'sslVerifyServerCert' is set to true,
  splunkd is also willing to verify certificates which have a
  so-called "Subject Alternate Name" that matches any of the alternate
  names in this list.
* Subject Alternate Names are effectively extended descriptive
  fields in SSL certs beyond the commonName.  A common practice for
  HTTPS certs is to use these values to store additional valid
  hostnames or domains where the cert should be considered valid.
* Accepts a comma-separated list of Subject Alternate Names to consider
  valid.
* Items in this list are never validated against the SSL Common Name.
* Default: Some alternate name checking

disabled = <boolean>
* Select true to disable this feature or false to enable this feature. App
  licensing is experimental, so it is disabled by default.
* Default: true

############################################################################
# License manager settings for configuring the license pool(s)
############################################################################

[license]
master_uri = [self|<uri>]
* An example of <uri>: <scheme>://<hostname>:<port>

active_group = Enterprise|Trial|Forwarder|Free
* These timeouts only matter if you have a master_uri set to remote master
connection_timeout = 30
* Maximum time, in seconds, to wait before connection to master times out.

send_timeout = <integer>
* Maximum time, in seconds, to wait before sending data to master times out
* Default: 30

receive_timeout = <integer>
* Maximum time, in seconds, to wait before receiving data from master times
  out
* Default: 30

squash_threshold = <positive integer>
* Advanced setting.  Periodically the indexer must report to license manager
  the data indexed broken down by source, sourcetype, host, and index.  If
  the number of distinct (source, sourcetype, host, index) tuples grows over
  the squash_threshold, we squash the (host, source) values and only report a
  breakdown by (sourcetype, index).  This is to prevent explosions in
  memory + license_usage.log lines.  Set this only after consulting a Splunk
  Support engineer.  This needs to be set on license slaves as well as license
  master.
* Default: 2000

report_interval = <nonnegative integer>[s|m|h]
* Selects a time period for reporting in license usage to the license
  master.
* This value is intended for very large deployments (hundreds of indexers)
  where a large number of indexers may overwhelm the license server.
* The maximum permitted interval is 1 hour.
* The minimum permitted interval is 1 minute.
* Can be expressed as a positive number of seconds, minutes or hours.
* If no time unit is provided, seconds is assumed.
* Default: 1m

strict_pool_quota = <boolean>
* Toggles strict pool quota enforcement
* If set to true, members of pools receive warnings for a given day if
  usage exceeds pool size regardless of whether overall stack quota was
  exceeded
* If set to false, members of pool only receive warnings if both pool
  usage exceeds pool size AND overall stack usage exceeds stack size
* Default: true

pool_suggestion = <string>
* Suggest a pool to the master for this slave.
* The master uses this suggestion if the master doesn't have an explicit
  rule mapping the slave to a given pool (ie...no slave list for the
  relevant license stack contains this slave explicitly)
* If the pool name doesn't match any existing pool, it is ignored, no
  error is generated
* This setting is intended to give an alternative management option for
  pool/slave mappings.  When onboarding an indexer, it may be easier to
  manage the mapping on the indexer itself via this setting rather than
  having to update server.conf on master for every addition of new indexer
* NOTE: If you have multiple stacks and a slave maps to multiple pools, this
        feature is limited in only allowing a suggestion of a single pool;
        This is not a common scenario however.
* No default. (which means this feature is disabled)

[lmpool:auto_generated_pool_forwarder]
* This is the auto generated pool for the forwarder stack

description = <textual description of this license pool>
quota = MAX|<maximum amount allowed by this license>
* MAX indicates the total capacity of the license. You may have only 1 pool
  with MAX size in a stack
* The quota can also be specified as a specific size eg. 20MB, 1GB etc

slaves = *|<slave list>
* An asterisk(*) indicates that any slave can connect to this pool
* You can also specify a comma separated slave guid list

stack_id = forwarder
* The stack to which this pool belongs.

[lmpool:auto_generated_pool_free]
* This is the auto generated pool for the free stack
* Field descriptions are the same as that for
  the 'lmpool:auto_generated_pool_forwarder' setting.

[lmpool:auto_generated_pool_enterprise]
* This is the auto generated pool for the enterprise stack
* Field descriptions are the same as that for
  the 'lmpool:auto_generated_pool_forwarder' setting.


[lmpool:auto_generated_pool_fixed-sourcetype_<sha256 hash of srctypes>]
* This is the auto generated pool for the enterprise fixed srctype stack
* Field descriptions are the same as that for
  the 'lmpool:auto_generated_pool_forwarder' setting.

[lmpool:auto_generated_pool_download_trial]
* This is the auto generated pool for the download trial stack
* Field descriptions are the same as that for
  the "lmpool:auto_generated_pool_forwarder"

############################################################################
#
# Search head pooling configuration
#
# Changes to a search head's pooling configuration must be made to the file:
#
#  $SPLUNK_HOME/etc/system/local/server.conf
#
# In other words, you can not deploy the [pooling] stanza using an app, either
# on local disk or on shared storage.
#
# This is because these values are read before the configuration system
# itself has been completely initialized. Take the value of the 'storage'
# setting, for example.  This value cannot be placed in an app on 
# shared storage because Splunk must use this value to find shared storage 
# in the first place!
#
############################################################################

[pooling]

state = [enabled|disabled]
* Enables or disables search head pooling.
* Default: disabled

storage = <path to shared storage>
* All members of a search head pool must have access to shared storage.
* Splunk software stores configurations and search artifacts here.
* On *NIX, this should be an NFS mount.
* On Windows, this should be a UNC path to a Samba/CIFS share.

app_update_triggers = true|false|silent
* Should this search head run update triggers for apps modified by other
  search heads in the pool?
* For more information about update triggers specifically, see the
  [triggers] stanza in the
  $SPLUNK_HOME/etc/system/README/app.conf.spec
  file.
* If set to true, this search head attempts to reload inputs, indexes,
  custom REST endpoints, etc. stored within apps that are installed,
  updated, enabled, or disabled by other search heads.
* If set to false, this search head does not run any update triggers. Note
  that this search head still detects configuration changes and app
  state changes made by other search heads. It simply does not reload any
  components within Splunk that might care about those changes, like input
  processors or the HTTP server.
* If set to silent, is like setting a value of 'true', with one
  difference: update triggers never result in restart banner messages
  or restart warnings in the UI. Any need to restart is instead be
  signaled only by messages in splunkd.log.
* Default: true

lock.timeout = <time range string>
* Timeout, in seconds, for acquiring file-based locks on configuration files.
* Splunk software waits up to this amount of time before aborting a
  configuration write.
* Default: 10s

lock.logging = <boolean>
* When acquiring a file-based lock, log information into the locked file.
* This information typically includes:
  * Which host is acquiring the lock
  * What that host intends to do while holding the lock
* There is no maximum filesize or rolling policy for this logging. If you
  enable this setting, you must periodically truncate the locked file
  yourself to prevent unbounded growth.
* The information logged to the locked file is intended for debugging
  purposes only. Splunk makes no guarantees regarding the contents of the
  file. It may, for example, write padding NULs to the file or truncate the
  file at any time.
* Default: false


############################################################################
# The following two intervals interrelate; the longest possible time for a
# state change to travel from one search pool member to the rest should be
# approximately the sum of these two timers.
############################################################################

poll.interval.rebuild = <time range string>
* Rebuild or refresh in-memory configuration data structures at most this
  often.
* Default: 1m (1 minute)

poll.interval.check = <time range string>
* Check on-disk configuration files for changes at most this often.
* Default: 1m (1 minute)

poll.blacklist.<name> = <regex>
* Do not check configuration files for changes if they match this regular
  expression.
* Example: Do not check vim swap files for changes -- .swp$


############################################################################
# High availability clustering configuration
############################################################################

[clustering]

mode = [master|slave|searchhead|disabled]
* Sets operational mode for this cluster node.
* Only one master may exist per cluster.
* Default: disabled

master_uri = [<uri> | clustermaster:stanzaName1, clustermaster:stanzaName2]
* Only valid for 'mode=slave' or 'mode=searchhead'.
* The URI of the cluster master that this slave or search head 
  should connect to.
* An example of <uri>: <scheme>://<hostname>:<port>
* Only for 'mode=searchhead' - If the search head is a part of multiple
  clusters, the master URIs can be specified by a comma separated list.

advertised_disk_capacity = <integer>
* Percentage to use when advertising disk capacity to the cluster master.
  This is useful for modifying weighted load balancing in indexer discovery.
* For example, if you set this attribute to 50 for an indexer with a 
  500GB disk, the indexer advertises its disk size as 250GB, not 500GB.
* Acceptable value range is 10 to 100.
* Default: 100

pass4SymmKey = <password>
* Secret shared among the nodes in the cluster to prevent any
  arbitrary node from connecting to the cluster. If a slave or
  search head is not configured with the same secret as the master,
  it is not able to communicate with the master.
* If it is not set in the [clustering] stanza, the key 
  is looked in the [general] stanza
* Unencrypted passwords must not begin with "$1$", as this is used by
  Splunk software to determine if the password is already encrypted.
* No default.

service_interval = <zero or positive integer>
* Only valid when "mode=master".
* Specifies, in seconds, how often the master runs its service
  loop. In its service loop, the master checks the state of the
  peers and the buckets in the cluster and also schedules
  corrective action, if possible, for buckets that are not in
  compliance with replication policies.
* A special default value of 0 indicates an auto mode where the service 
  interval for the next service call is determined by the time taken by 
  previous call.
* Service interval is bounded by the values 1 and 
  the 'max_auto_service_interval' setting.
  If previous service call takes more than 'max_auto_service_interval' 
  seconds, next service interval is set to 
  'max_auto_service_interval' seconds.
* Default: 0

max_fixup_time_ms = <zero or positive integer>
* Only valid for 'mode=master'. 
* Specifies, in milliseconds, how long each fixup level runs before 
  short circuiting to continue to the next fixup level. This 
  introduces an upper-bound on each service level, and likewise 
  introduces an upper bound on the full service() call.
* This setting is useful for larger clusters that have lots of 
  buckets, where service() calls can consume a significant amount 
  of time blocking other operations.
* 0 denotes that there is no max fixup timer.
* Default: 0

cxn_timeout = <integer>
* Lowlevel timeout, in seconds, for establishing connection between 
  cluster nodes.
* Default: 60

send_timeout = <integer>
* Lowlevel timeout, in seconds, for sending data between cluster nodes.
* Default: 60

rcv_timeout = <integer>
* Lowlevel timeout, in seconds, for receiving data between cluster nodes.
* Default: 60

rep_cxn_timeout = <integer>
* Lowlevel timeout, in seconds, for establishing connection for replicating data.
* Default: 5

rep_send_timeout = <integer>
* Lowlevel timeout, in seconds, for sending replication slice data between 
  cluster nodes.
* This is a soft timeout. When this timeout is triggered on source peer,
  it tries to determine if target is still alive. If it is still alive, it
  reset the timeout for another 'rep_send_timeout interval' and continues.  If
  target has failed or cumulative timeout has exceeded the 
  'rep_max_send_timeout', replication fails.
* Default: 5

rep_rcv_timeout = <integer>
* Lowlevel timeout, in seconds, for receiving acknowledgment data from peers.
* This is a soft timeout. When this timeout is triggered on source peer,
  it tries to determine if target is still alive. If it is still alive,
  it reset the timeout for another 'rep_send_timeout' interval and continues.
* If target has failed or cumulative timeout has exceeded
  'rep_max_rcv_timeout', replication fails.
* Default: 10

search_files_retry_timeout = <integer>
* Timeout, in seconds, after which request for search files from a 
  peer is aborted.
* To make a bucket searchable, search specific files are copied from 
  another source peer with search files. If search files on source 
  peers are undergoing chances, it asks requesting peer to retry after 
  some time. If cumulative retry period exceeds the specified timeout, 
  the requesting peer aborts the request and requests search files from 
  another peer in the cluster that may have search files.
* Default: 600 (10 minutes)

re_add_on_bucket_request_error = <boolean>
* Valid only for 'mode=slave'.
* If set to true, slave re-adds itself to the cluster master if
  cluster master returns an error on any bucket request. On re-add,
  slave updates the master with the latest state of all its buckets.
* If set to false, slave doesn't re-add itself to the cluster master.
  Instead, it updates the master with those buckets that master
  returned an error.
* Default: false
 
decommission_search_jobs_wait_secs = <integer>
* Valid only for mode=slave
* Determines maximum time, in seconds, that a peer node waits for search
  jobs to finish before it transitions to the down (or) GracefulShutdown 
  state, in response to the 'splunk offline' (or)   
  'splunk offline --enforce-counts' command.
* Default: 180 (3 minutes)

decommission_node_force_timeout = <seconds>
* Valid only for mode=slave and during node offline operation
* The maximum time, in seconds, that a peer node waits for searchable copy reallocation
  jobs to finish before it transitions to the down (or) GracefulShutdown state.
* This period begins after the peer node receives a 'splunk offline' command
  or its '/cluster/slave/control/control/decommission' REST endpoint is accessed.
* This attribute is not applicable to the  "--enforce-counts" version of the “splunk offline" command
* Defaults to 300 seconds.

decommission_force_finish_idle_time = <zero or positive integer>
* Valid only for mode=master.
* Time in minutes the master waits before forcibly finishing the
  decommissioning of a peer when there is no progress in the associated 
  fixup activity.
* A value of zero (0) means that the master does not forcibly finish 
  decommissioning.
* Default: 0

rolling_restart = restart|shutdown|searchable|searchable_force
* Only valid for 'mode=master'.
* Determines whether indexer peers restart or shutdown during a rolling
  restart.
* If set to restart, each peer automatically restarts during a rolling
  restart.
* If set to shutdown, each peer is stopped during a rolling restart,
  and the customer must manually restart each peer.
* If set to searchable, the cluster attempts a best-effort to maintain
  a searchable state during the rolling restart by reassigning primaries
  from peers that are about to restart to other searchable peers, and
  performing a health check to ensure that a searchable rolling restart is
  possible.
* If set to searchable_force, the cluster performs a searchable
  rolling restart, but overrides the health check and enforces
  'decommission_force_timeout' and 'restart_inactivity_timeout'.
* If set to searchable or searchable_force, scheduled searches
  are deferred or run during the rolling restart based on the
  'defer_scheduled_searchable_idx' setting in savedsearches.conf.
* Default: restart.

site_by_site = <boolean>
* Only valid for mode=master and multisite=true.
* If set to true, the master restarts peers from one site at a time,
  waiting for all peers from a site to restart before moving on to another
  site, during a rolling restart.
* If set to false, the master randomly selects peers to restart, from
  across all sites, during a rolling restart.
* Default: true.

decommission_force_timeout = <zero or positive integer>
* Only valid for rolling_restart=searchable_force
* The amount of time, in seconds, the cluster master waits for a
  peer in primary decommission status to finish primary reassignment
  and restart, during a searchable rolling restart with timeouts.
* Differs from decommission_force_finish_idle_time in its default value
  and its presence only during a searchable rolling restart with timeouts.
* If you set this parameter to 0, it is automatically reset 
  to default value.
* Maximum accepted value is 1800 (30 minutes).
* Default: 180 (3 minutes)

restart_inactivity_timeout = <zero or positive integer>
* Only valid for rolling_restart=searchable_force
* The amount of time, in seconds, that the master waits for a peer to
  restart and rejoin the cluster before it considers the restart a failure
  and proceeds to restart other peers.
* A value of zero (0) means that the master waits indefinitely for a peer
  to restart.
* Default: 600 (10 minutes)

rep_max_send_timeout = <integer>
* Maximum send timeout, in seconds, for sending replication slice 
  data between cluster nodes.
* On rep_send_timeout source peer determines if total send timeout has
  exceeded 'rep_max_send_timeout'. If so, replication fails.
* If cumulative 'rep_send_timeout' exceeds 'rep_max_send_timeout', 
  replication
  fails.
* Default: 180 (3 minutes)

rep_max_rcv_timeout = <integer>
* Maximum cumulative receive timeout, in seconds, for receiving 
  acknowledgment data from peers.
* On 'rep_rcv_timeout' source peer determines if total 
  receive timeout has exceeded 'rep_max_rcv_timeout'. 
  If so, replication fails.
* Default: 180 (3 minutes)

multisite = <boolean>
* Turns on the multisite feature for this master.
* Make sure you set site parameters on the peers when you turn this to true.
* Default: false

replication_factor = <positive integer>
* Only valid for mode=master.
* Determines how many copies of rawdata are created in the cluster.
* Use site_replication_factor instead of this in case 'multisite' 
  is turned on.
* Must be greater than 0.
* Default: 3

site_replication_factor = <comma-separated string>
* Only valid for 'mode=master' and is only used if 'multisite=true'.
* This specifies the per-site replication policy for any given
  bucket represented as a comma-separated list of per-site entries.
* Currently specified globally and applies to buckets in all
  indexes.
* Each entry is of the form <site-id>:<positive integer> which
  represents the number of copies to make in the specified site
* Valid site-ids include two mandatory keywords and optionally
  specific site-ids from site1 to site63
* The mandatory keywords are:
  - origin: Every bucket has a origin site which is the site of
  the peer that originally created this bucket. The notion of
  'origin' makes it possible to specify a policy that spans across
  multiple sites without having to enumerate it per-site.
  - total: The total number of copies we want for each bucket.
* When a site is the origin, it could potentially match both the
  origin and a specific site term. In that case, the max of the
  two is used as the count for that site.
* The total must be greater than or equal to sum of all the other
  counts (including origin).
* The difference between total and the sum of all the other counts
  is distributed across the remaining sites.
* Example 1: site_replication_factor = origin:2, total:3
  Given a cluster of 3 sites, all indexing data, every site has 2
  copies of every bucket ingested in that site and one rawdata
  copy is put in one of the other 2 sites.
* Example 2: site_replication_factor = origin:2, site3:1, total:3
  Given a cluster of 3 sites, 2 of them indexing data, every
  bucket has 2 copies in the origin site and one copy in site3. So
  site3 has one rawdata copy of buckets ingested in both site1 and
  site2 and those two sites have 2 copies of their own buckets.
* Default: origin:2, total:3

search_factor = <positive integer>
* Only valid for 'mode=master'.
* Determines how many buckets have index structures pre-built.
* Must be less than or equal to the 'replication_factor' setting and 
  greater than 0.
* Default: 2

site_search_factor = <comma-separated string>
* Only valid for 'mode=master' and is only used if 'multisite=true'.
* This specifies the per-site policy for searchable copies for any
  given bucket represented as a comma-separated list of per-site
  entries.
* This is similar to the 'site_replication_factor' setting. 
  Please see that entry for more information on the syntax.
* Default: origin:1, total:2

available_sites = <comma-separated string>
* Only valid for 'mode=master' and is only used if 'multisite=true'.
* This is a comma-separated list of all the sites in the cluster.
* If 'multisite=true' then 'available_sites' must be 
  explicitly set.
* Default: an empty string

forwarder_site_failover = <comma-separated string>
* Only valid for mode=master and is only used if 'multisite=true'.
* This is a comma-separated list of pair of sites, "site1:site2", 
  in the cluster.
* If 'multisite' is turned on 'forwarder_site_failover' must be 
  explicitly set.
* Default: an empty string

site_mappings = <comma-separated string>
* Only valid for mode=master
* When you decommission a site, you must update this attribute so that the 
  origin bucket copies on the decommissioned site are mapped to a remaining 
  active site. This attribute maps decommissioned sites to active sites. 
  The bucket copies for which a decommissioned site is the origin site
  are then replicated to the active site specified by the mapping.
* Used only if multisite is true and sites have been decommissioned.
* Each comma-separated entry is of the form 
  <decommissioned_site_id>:<active_site_id>
  or default_mapping:<default_site_id>.
  <decommissioned_site_id> is a decommissioned site and <active_site_id> is 
  an existing site,specified in the 'available_sites' setting.
  For example, if available_sites=site1,site2,site3,site4 and you 
  decommission site2, you can map site2 to a remaining site such as site4, 
  like this: site2:site4 .
* If a site used in a mapping is later decommissioned, its previous mappings 
  must be remapped to an available site. For instance, if you have the 
  mapping site1:site2 but site2 is later decommissioned, you can remap 
  both site1 and site2 to an active site3 using the following replacement 
  mappings - site1:site3,site2:site3.
* Optional entry with syntax default_mapping:<default_site_id> represents the
  default mapping, for cases where an explicit mapping site is not specified.
  For example: default_mapping:site3 maps any decommissioned site to site3, 
  if they are not otherwise explicitly mapped to a site.
  There can only be one such entry.
* Example 1: site_mappings = site1:site3,default_mapping:site4.
  The cluster must include site3 and site4 in available_sites, and site1 
  must be decommissioned.
  The origin bucket copies for decommissioned site1 is mapped to site3.
  Bucket copies for any other decommissioned sites is mapped to site4.
* Example 2: site_mappings = site2:site3
  The cluster must include site3 in available_sites, and site2 must be 
  decommissioned. The origin bucket copies for decommissioned site2 is 
  mapped to site3. This cluster has no default.
* Example 3: site_mappings = default_mapping:site5
  The above cluster must include site5 in available_sites.
  The origin bucket copies for any decommissioned sites is mapped onto 
  site5.
* Default: an empty string

constrain_singlesite_buckets = <boolean>
* Only valid for mode=master and is only used if multisite is true.
* Specifies whether the cluster keeps single-site buckets within one site
  in multisite clustering.
* When this setting is "true", buckets in a single site cluster do not
  replicate outside of their site. The buckets follow 'replication_factor'
  'search factor' policies rather than 'site_replication_factor'
  'site_search_factor' policies. This is to mimic the behavior of
  single-site clustering.
* When this setting is "false", buckets in non-multisite clusters can
  replicate across sites, and must meet the specified
  'site_replication_factor' and 'site_search_factor' policies.
* Default: true

heartbeat_timeout = <positive integer>
* Only valid for 'mode=master'.
* Specifies, in seconds, when the master considers a slave down. After a 
  slave is down, the master initiates fixup steps to replicate
  buckets from the dead slave to its peers.
* Default: 60

access_logging_for_heartbeats = <boolean>
* Only valid for 'mode=master'.
* Enables/disables logging to the splunkd_access.log file for peer 
  heartbeats.
* NOTE: you do not have to restart master to set this config parameter.
  Simply run the cli command on master:
    % splunk edit cluster-config -access_logging_for_heartbeats <<boolean>>
* Default: false (logging disabled)


restart_timeout = <positive integer>
* Only valid for 'mode=master'.
* This is the amount of time, in seconds, the master waits for a peer 
  to come back when the peer is restarted (to avoid the overhead of
  trying to fixup the buckets that were on the peer).
* Note that this only works with the offline command or if the peer
  is restarted vi the UI.
* Default: 60

quiet_period = <positive integer>
* Only valid for 'mode=master'.
* This determines the amount of time, in seconds, for which the 
  master is quiet right after it starts. During this period the master 
  does not initiate any action but is instead waiting for the slaves to
  register themselves. At the end of this time period, it builds
  its view of the cluster based on the registered information and
  starts normal processing.
* Default: 60

reporting_delay_period = <positive integer>
* Only valid for 'mode=master'.
* The acceptable amount of delay, in seconds, for reporting both unmet
  search and unmet replication factors for newly created buckets.
* This setting helps provide more reliable cluster status reporting
  by limiting updates to the specified granularity.
* Default: 30

generation_poll_interval = <positive integer>
* How often, in seconds, the search head polls the master for 
  generation information.
* This setting is valid only if 'mode=master' or 'mode=searchhead'.
* Default: 5

max_peer_build_load = <integer>
* This is the maximum number of concurrent tasks to make buckets
  searchable that can be assigned to a peer.
* Default: 2

max_peer_rep_load = <integer>
* This is the maximum number of concurrent non-streaming
  replications that a peer can take part in as a target.
* Default: 5

max_peer_sum_rep_load = <integer>
* This is the maximum number of concurrent summary replications
  that a peer can take part in as either a target or source.
* Default: 5

max_nonhot_rep_kBps = <integer>
* This is the maximum throughput (kB(Bytes)/s) for warm/cold/summary 
* replications on a specific source peer. Similar to forwarder's maxKBps 
* setting in the limits.conf file.
* This setting throttles total bandwidth consumption for all 
  outgoing non-hot replication connections from a given source peer. 
  It does not throttle at the 'per-replication-connection', per-target 
  level.
* This setting is reloadable without restart if manually updated on the 
  source peers by using the command "splunk edit cluster-config" 
  or by making the corresponding REST call. We don't recommend updating 
  this setting across all the peers using bundle push because: 
    1) The push requires a rolling restart, as do all bundle pushes 
       with the server.conf file change.
    2) You might want to set different values on different peers.
* If set to 0, signifies unlimited throughput.
* Default: 0

max_replication_errors = <integer>
* Only valid for 'mode=slave'.
* This is the maximum number of consecutive replication errors
  (currently only for hot bucket replication) from a source peer
  to a specific target peer. Until this limit is reached, the
  source continues to roll hot buckets on streaming failures to
  this target. After the limit is reached, the source no
  longer rolls hot buckets if streaming to this specific target
  fails. This is reset if at least one successful (hot bucket)
  replication occurs to this target from this source.
* The special value of 0 turns off this safeguard; so the source
  always rolls hot buckets on streaming error to any target.
* Default: 3

searchable_targets = <boolean>
* Only valid for 'mode=master'.
* Tells the master to make some replication targets searchable
  even while the replication is going on. This only affects
  hot bucket replication for now.
* Default: true

searchable_target_sync_timeout = <integer>
* Only valid for 'mode=slave'.
* If a hot bucket replication connection is inactive for this time,
  in seconds, a searchable target flushes out any pending search
  related in-memory files.
* Regular syncing - when the data is flowing through
  regularly and the connection is not inactive - happens at a
  faster rate (default of 5 secs controlled by
  streamingTargetTsidxSyncPeriodMsec in indexes.conf).
* The special value of 0 turns off this timeout behavior.
* Default: 60

target_wait_time = <positive integer>
* Only valid for 'mode=master'.
* Specifies the time, in seconds, that the master waits for the 
  target of a replication to register itself before it services 
  the bucket again and potentially schedules another fixup.
* Default: 150 (2 minutes 30 seconds)

summary_wait_time = <positive integer>
* Only valid when 'mode=master' and 'summary_replication=true'.
* Specifies the time, in seconds, that the master waits before 
  scheduling fixups for a newly 'done' summary that transitioned 
  from 'hot_done'. This allows for other copies of the 'hot_done' 
  summary to also make their transition into 'done', avoiding 
  unnecessary replications.
* Default: 660 (11 minutes)

commit_retry_time = <positive integer>
* Only valid for 'mode=master'.
* Specifies the interval, in seconds, after which, if the last 
  generation commit failed, the master forces a retry. A retry is usually 
  automatically kicked off after the appropriate events. This is just 
  a backup to make sure that the master does retry no matter what.
* Default: 300 (5 minutes)

percent_peers_to_restart = <integer between 0-100>
* Suggested percentage of maximum peers to restart for rolling-restart.
* Actual percentage may vary due to lack of granularity for smaller peer
  sets.
* Regardless of setting, a minimum of 1 peer is restarted per round.

max_peers_to_download_bundle = <positive integer>
* Only valid for mode=master
* Maximum no. of peers to simultaneously download the configuration bundle
  from the master, in response to the 'splunk apply cluster-bundle' command.
* When a peer finishes the download, the next waiting peer, if any, begins 
  its download. 
* If set to 0,  all peers try to download at once.
* Default: 0

auto_rebalance_primaries = <boolean>
* Only valid for 'mode=master'.
* Specifies if the master should automatically rebalance bucket
  primaries on certain triggers. Currently the only defined
  trigger is when a peer registers with the master. When a peer
  registers, the master redistributes the bucket primaries so the
  cluster can make use of any copies in the incoming peer.
* Default: true

idle_connections_pool_size = <integer>
* Only valid for 'mode=master'.
* Specifies how many idle http(s) connections we should keep alive to reuse.
  Reusing connections improves the time it takes to send messages to peers
  in the cluster.
* -1 corresponds to "auto", letting the master determine the
  number of connections to keep around based on the number of peers in the
  cluster.
* Default: -1

use_batch_mask_changes = <boolean>
* Only valid for mode=master
* Specifies if the master should process bucket mask changes in
  batch or individually one by one.
* Set to false when there are version 6.1 peers in the cluster for backwards 
  compatibility.
* Default: true

service_jobs_msec = <positive integer>
* Only valid for 'mode=master'.
* Max time, in milliseconds, that the cluster master spends in servicing 
  finished jobs for each service call. Increase this if the metrics.log file
  has very high 'current_size' values.
* Default: 100 (0.1 seconds)

summary_replication = true|false|disabled
* Valid for both 'mode=master' and 'mode=slave'.
* Cluster Master:
  If set to true, summary replication is enabled.
  If set to false, summary replication is disabled, but can be enabled at runtime.
  Ff set to disabled, summary replication is disabled. Summary replication 
  cannot be enabled at runtime.
* Peers:
  If set to true or false, there is no effect. The indexer follows
  whatever setting is on the Cluster Master.
  If set to disabled, summary replication is disabled. The indexer does 
  no scanning of summaries (increased performance during peers joing 
  the cluster for large clusters).
* Default: false (for both Cluster Master and Peers)

rebalance_threshold = <number between 0.10 and 1.00>
* Only valid for mode=master'.
* During rebalancing buckets amongst the cluster, this threshold is 
  used as a percentage to determine when the cluster is balanced.
* 1.00 is 100% indexers fully balanced.

max_auto_service_interval = <positive integer>
* Only valid for 'mode=master'.
* Only valid when 'service_interval' is in auto mode.
  For example service_interval=0.
* Indicates the maximum value, in seconds, that service interval is 
  bounded by when the 'service_interval' is in auto mode. If the 
  previous service call took more than 'max_auto_service_interval' 
  seconds, the next service call runs after 'max_auto_service_interval' 
  seconds.
* NOTE: It is highly recommended that you choose a value that is one-half
  of the smaller of 'heartbeat_timeout' or 'restart_timeout'. For example,
  the default value of 30 is based on the default value of 60 for both
  'heartbeat_timeout' and 'restart_timeout'.
* Default: 30
 
buckets_to_summarize = <primaries|primaries_and_hot|all>
* Only valid for 'mode=master'.
* Determines which buckets we send '| summarize' searches (searches that build
  report acceleration and data models). 'primaries' applies it to only primary
  buckets, while 'primaries_and_hot' also applies it to all hot searchable
  buckets. 'all' applies the search to all buckets.
* If 'summary_replication' is enabled, then 'buckets_to_summarize' defaults 
  to 'primaries_and_hot'.
* Do not change this setting without first consulting with Splunk Support.
* Default: primaries

maintenance_mode = <boolean>
* Only valid for 'mode=master'.
* To preserve the maintenance mode setting in case of master
  restart, the master automatically updates this setting in the
  etc/system/local/server.conf file whenever the user enables or disables
  maintenance mode using CLI or REST.
* NOTE: Do not manually update this setting. Instead use CLI or REST
  to enable or disable maintenance mode.

backup_and_restore_primaries_in_maintenance = <boolean>
* Only valid for 'mode=master'.
* Determines whether the master performs a backup/restore of bucket 
  primary masks during maintenance mode or rolling-restart of cluster peers.
* If set to true, restoration of primaries occurs automatically when the peers
  rejoin the cluster after a scheduled restart or upgrade.
* Default: false

max_primary_backups_per_service = <zero or positive integer>
* Only valid for 'mode=master'.
* For use with the "backup_and_restore_primaries_in_maintenance" setting.
* Determines the number of peers for which the master backs up primary
  masks for each service call.
* The special value of 0 causes the master to back up the primary masks for
  all peers in a single service call.
* Default: 10

allow_default_empty_p4symmkey = <boolean>
* Only valid for 'mode=master'.
* Affects behavior of master during start-up, if 'pass4SymmKey'resolves 
  to the null string or the default password ("changeme").
* If set to true, the master posts a warning but still launches.
* If set to false, the master posts a warning and stops.
* Default: true

register_replication_address = <IP address, or fully qualified machine/domain name>
* Only valid for 'mode=slave'.
* This is the address on which a slave is available for accepting
  replication data. This is useful in the cases where a slave host machine
  has multiple interfaces and only one of them can be reached by another
  splunkd instance

register_forwarder_address = <IP address, or fully qualified machine/domain name>
* Only valid for 'mode=slave'.
* This is the address on which a slave is available for accepting
  data from forwarder.This is useful in the cases where a splunk host
  machine has multiple interfaces and only one of them can be reached by
  another splunkd instance.

register_search_address = <IP address, or fully qualified machine/domain name>
* Only valid for 'mode=slave'
* This is the address on which a slave is available as search head.
  This is useful in the cases where a splunk host machine has multiple
  interfaces and only one of them can be reached by another splunkd
  instance.

executor_workers = <positive integer>
* Only valid if 'mode=master' or 'mode=slave'.
* Number of threads that can be used by the clustering thread pool.
* A value of 0 defaults to 1.
* Default: 10 

local_executor_workers = <positive integer>
* Only valid if 'mode=slave'
* Number of threads that can be used by the local clustering thread pool.
* executor_workers is used mostly for communication between the peer
  and the master. local_executor_workers are used for any jobs that
  must be spawned to take care of housekeeping tasks only related
  to the peer such as a peer synchronizing itself with remote storage.
* A value of 0 defaults to 1.
* Default: 10 

manual_detention = on|on_ports_enabled|off
* Only valid for 'mode=slave'.
* Puts this peer node in manual detention.
* Default: off

allowed_hbmiss_count = <non-zero positive integer>
* Only valid for 'mode=slave'.
* Sets the count of number of heartbeat failures before the peer node
  disconnects from the master.
* Default: 3 

buckets_per_addpeer = <non-negative integer>
* Only valid for 'mode=slave'.
* Controls the number of buckets for each add peer request.
* When a peer is added or re-added to the cluster, it sends the master
  information for each of its buckets. Depending on the number of buckets,
  this could take a while. For example, a million buckets could require
  more than a minute of the master's processing time. To prevent the master
  from being occupied by this single task too long, you can use this setting to
  split large numbers of buckets into several"batch-add-peer" requests.
* If it is invalid or non-existant, the peer uses the default setting instead.
* If it is set to 0, the peer sends only one request with all buckets
  instead of batches.
* Default: 1000

heartbeat_period = <non-zero positive integer>
* Only valid for 'mode=slave'.
* Controls the frequency the slave attempts to send heartbeats.

remote_storage_upload_timeout = <non-zero positive integer>
* Only valid for 'mode=slave'.
* For a remote storage enabled index, this attribute specifies the interval
  in seconds, after which target peers assume responsibility for 
  uploading a bucket to the remote storage, if they do not hear from 
  the source peer.
* Default: 300 (5 minutes)

remote_storage_retention_period = <non-zero positive integer>
* Only valid for 'mode=master'.
* Controls the length, in seconds, of peer-node retention for buckets in
  remote storage enabled indexes. When this length is exceeded, the master
  freezes the buckets on the peer nodes.
* Default: 900 (15 minutes)

recreate_bucket_attempts_from_remote_storage = <positive integer>
* Only valid for 'mode=master'.
* Controls the number of attempts the master makes to recreate the
  bucket of a remote storage enabled index on a random peer node
  in these scenarios:
    * Master detects that the bucket is not present on any peers.
    * A peer informs the master about the bucket as part of the
      re-creation of an index.
      See recreate_index_attempts_from_remote_storage attribute.
* Re-creation of the bucket involves the following steps:
    1. Master provides a random peer with the bucket ID of the bucket that
       needs to be recreated.
    2. Peer fetches the metadata of the bucket corresponding to this
       bucket ID from the remote storage.
    3. Peer creates a bucket with the fetched metadata locally and informs
       the master that a new bucket has been added.
    4. Master initiates fix-ups to add the bucket on the necessary number
       of additional peers to match the replication and search factors.
* If set to 0, disables the re-creation of the bucket.
* Default: 10

recreate_bucket_fetch_manifest_batch_size = <positive integer>
* Only valid for 'mode=master'.
* Controls the maximum number of bucket IDs for which a slave 
  attempts to initiate a parallel fetch of manifests at a time
  in the process of recreating buckets that have been
  requested by the master.
* The master sends this setting to all the slaves that are
  involved in the process of recreating the buckets.
* Default: 50

recreate_index_attempts_from_remote_storage = <positive integer>
* Only valid for 'mode=master'.
* Controls the number of attempts the master makes to recreate
  a remote storage enabled index on a random peer node when the master
  is informed about the index by a peer.
* Re-creation of an index involves the following steps:
    1. Master pushes a bundle either when it is ready for service or
       when requested by the user.
    2. Master waits for the bundle to be applied successfully on the
       peer nodes.
    3. Master requests that a random peer node provide it with the list
       of newly added remote storage enabled indexes.
    4. Master distributes a subset of indexes from this list to
       random peer nodes.
    5. Each of those peer nodes fetches the list of bucket IDs for the
       requested index from the remote storage and provides it
       to the master.
    6. The master uses the list of bucket IDs to recreate the buckets.
       See recreate_bucket_attempts_from_remote_storage.
* If set to 0, disables the re-creation of the index.
* Default: 10

recreate_index_fetch_bucket_batch_size = <positive integer>
* Only valid for 'mode=master'.
* Controls the maximum number of bucket IDs that the master 
  requests a random peer node to fetch from remote storage as part of
  a single transaction for a remote storage enabled index.
  The master uses the bucket IDs for re-creation of the index.
  See the 'recreate_index_attempts_from_remote_storage' setting.
* Default: 2000 

buckets_status_notification_batch_size = <positive integer>
* Only valid for 'mode=slave'.
* Controls the number of existing buckets IDs that the slave
  reports to the master every notify_scan_period seconds.
  The master then initiates fix-ups for these buckets.
* CAUTION: Do not modify this setting without guidance from 
  Splunk personnel.
* Default: 10

notify_scan_period = <non-zero positive integer>
* Only valid for 'mode=slave'.
* Controls the frequency, in seconds, that the indexer handles 
  the following options:
  1. buckets_status_notification_batch_size
  2. summary_update_batch_size
  3. summary_registration_batch_size
* CAUTION: Do not modify this setting without guidance from 
  Splunk personnel.
* Default: 10

notify_scan_min_period = <non-zero positive integer>
* Only valid for 'mode=slave'.
* Controls the highest frequency, in milliseconds, that the indexer 
  scans summary folders
  for summary updates/registrations. The notify_scan_period temporarily
  becomes notify_scan_min_period when there are more summary
  updates/registration events to be processed but has been limited due to
  either summary_update_batch_size or summary_registration_batch_size.
* CAUTION: Do not modify this setting without guidance from Splunk 
  personnel.
* Default: 10

summary_update_batch_size = <non-zero positive integer>
* Only valid for 'mode=slave'.
* Controls the number of summary updates the indexer sends per batch to
  the master every notify_scan_period.
* CAUTION: Do not modify this setting without guidance from 
  Splunk personnel.
* Default: 10

summary_registration_batch_size = <non-zero positive integer>
* Only valid for 'mode=slave'.
* Controls the number of summaries that get asynchronously registered
  on the indexer and sent as a batch to the master every
  notify_scan_period.
* Caution: Do not modify this setting without guidance from Splunk personnel.
* Default: 1000

enableS2SHeartbeat = true|false
* Only valid for 'mode=slave'.
* Splunk software monitors each replication connection for 
  presence of a heartbeat, and if the heartbeat is not seen for 's2sHeartbeatTimeout' seconds, it closes the connection.
* Default: true

s2sHeartbeatTimeout = <seconds>
* This specifies the global timeout value, in seconds, for monitoring 
  heartbeats on replication connections.
* Splunk software closes a replication connection if heartbeat is not seen
  for 's2sHeartbeatTimeout' seconds.
* Replication source sends heartbeats every 30 seconds.
* Default: 600 (10 minutes)

throwOnBucketBuildReadError = true|false
* Valid only for 'mode=slave'.
* If set to true, index clustering slave throws an exception if it 
  encounters a journal read error while building the bucket for a new 
  searchable copy. It also throws all the search & other files generated 
  so far in this particular bucket build.
* If set to false, index clustering slave just logs the error and preserves 
  all the search & other files generated so far & finalizes them as it 
  cannot proceed further with this bucket.
* Default: false

cluster_label = <string>
* This specifies the label of the indexer cluster

[clustermaster:<stanza>]
* Only valid for 'mode=searchhead' when the search head is a part of 
  multiple clusters.

master_uri = <uri>
* Only valid for 'mode=searchhead' when present in this stanza.
* URI of the cluster master that this search head should connect to.

pass4SymmKey = <password>
* Secret shared among the nodes in the cluster to prevent any
  arbitrary node from connecting to the cluster. If a search head
  is not configured with the same secret as the master,
  it not be able to communicate with the master.
* If it is not present here, the key in the clustering stanza is used.
  If it is not present in the clustering stanza, the value in the general
  stanza is used.
* Unencrypted passwords must not begin with "$1$", as this is used by
  Splunk software to determine if the password is already encrypted.
* No default.

site = <site-id>
* Specifies the site this search head belongs to for this particular master
  when multisite is enabled (see below).
* Valid values for site-id include site0 to site63.
* The special value "site0" disables site affinity for a search head in a 
  multisite cluster. It is only valid for a search head.

multisite = <boolean>
* Turns on the multisite feature for this master_uri for the search head.
* Make sure the master has the multisite feature turned on.
* Make sure you specify the site in case this is set to true. If no
  configuration is found in the [clustermaster] stanza, we default to any
  value for site that might be defined in the [general]
  stanza.
* Default: false

[replication_port://<port>]
# Configure Splunk to listen on a given TCP port for replicated data from
# another cluster member.
# If 'mode=slave' is set in the [clustering] stanza at least one
# 'replication_port' must be configured and not disabled.

disabled = true|false
* Set to true to disable this replication port stanza.
* Default: false

listenOnIPv6 = no|yes|only
* Toggle whether this listening port listens on IPv4, IPv6, or both.
* If not present, the setting in the [general] stanza is used.

acceptFrom = <network_acl> ...
* Lists a set of networks or addresses from which to accept connections.
* This setting only takes effect when 'appServerPorts' is set to a
  non-zero value.
* Separate multiple rules with commas or spaces.
* Each rule can be in one of the following formats:
    1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    2. A Classless Inter-Domain Routing (CIDR) block of addresses
       (examples: "10/8", "192.168.1/24", "fe80:1234/32")
    3. A DNS name, possibly with a "*" used as a wildcard
       (examples: "myhost.example.com", "*.splunk.com")
    4. "*", which matches anything
* You can also prefix an entry with '!' to cause the rule to reject the
  connection. The input applies rules in order, and uses the first one that
  matches.
  For example, "!10.1/16, *" allows connections from everywhere except
  the 10.1.*.* network.
* Default: "*" (accept from anywhere)

[replication_port-ssl://<port>]
* This configuration is same as the [replication_port] stanza above, 
  but uses SSL.

disabled = <boolean>
* Set to true to disable this replication port stanza.
* Default: false

listenOnIPv6 = no|yes|only
* Toggle whether this listening port listens on IPv4, IPv6, or both.
* If not present, the setting in the [general] stanza is used.

acceptFrom = <network_acl> ...
* This setting is the same as the setting in the [replication_port] stanza. 

serverCert = <path>
* Full path to file containing private key and server certificate.
* The <path> must refer to a PEM format file.
* No default.

sslPassword = <password>
* Server certificate password, if any.
* No default.

password = <password>
* DEPRECATED; use 'sslPassword' instead.

rootCA = <path>
* DEPRECATED; use '[sslConfig]/sslRootCAPath' instead.
* Full path to the root CA (Certificate Authority) certificate store.
* The <path> must refer to a PEM format file containing one or more root CA
  certificates concatenated together.
* No default.

cipherSuite = <cipher suite string>
* If set, uses the specified cipher string for the SSL connection.
* Must specify 'dhFile' to enable any Diffie-Hellman ciphers.
* Default: The default can vary. See the cipherSuite setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the current default.

sslVersions = <versions_list>
* Comma-separated list of SSL versions to support.
* The versions available are "ssl3", "tls1.0", "tls1.1", and "tls1.2".
* The special version "*" selects all supported versions.  The version "tls"
  selects all versions tls1.0 or newer.
* If a version is prefixed with "-" it is removed from the list.
* SSLv2 is always disabled; "-ssl2" is accepted in the version list but 
  does nothing.
* When configured in FIPS mode, ssl3 is always disabled regardless
  of this configuration.
* Default: The default can vary. See the sslVersions setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the current default.

ecdhCurves = <comma separated list of ec curves>
* ECDH curves to use for ECDH key negotiation.
* The curves should be specified in the order of preference.
* The client sends these curves as a part of Client Hello.
* The server supports only the curves specified in the list.
* We only support named curves specified by their SHORT names.
  (see struct ASN1_OBJECT in asn1.h)
* The list of valid named curves by their short/long names can be obtained
  by executing this command:
  $SPLUNK_HOME/bin/splunk cmd openssl ecparam -list_curves
* e.g. ecdhCurves = prime256v1,secp384r1,secp521r1
* Default: The default can vary. See the ecdhCurves setting in 
  the $SPLUNK_HOME/etc/system/default/server.conf file for the current default.

dhFile = <path>
* PEM format Diffie-Hellman parameter file name.
* DH group size should be no less than 2048bits.
* This file is required in order to enable any Diffie-Hellman ciphers.
* Not set by default.

dhfile = <path>
* DEPRECATED; use 'dhFile' instead.

supportSSLV3Only = <boolean>
* DEPRECATED.  SSLv2 is now always disabled.  The exact set of SSL versions
  allowed is now configurable by using  the 'sslVersions' setting above.

useSSLCompression = <boolean>
* If true, enables SSL compression.
* Default: true

compressed = <boolean>
* DEPRECATED. Use 'useSSLCompression' instead.
* Used only if 'useSSLCompression' is not set.

requireClientCert = <boolean>
* Requires that any peer that connects to replication port has a certificate
  that can be validated by certificate authority specified in rootCA.
* Default: false

allowSslRenegotiation = <boolean>
* In the SSL protocol, a client may request renegotiation of the connection
  settings from time to time.
* Setting this to false causes the server to reject all renegotiation
  attempts, breaking the connection.  This limits the amount of CPU a
  single TCP connection can use, but it can cause connectivity problems
  especially for long-lived connections.
* Default: true

sslCommonNameToCheck = <commonName1>, <commonName2>, ...
* Optional. 
* Check the common name of the client's certificate against this list of names.
* requireClientCert must be set to "true" for this setting to work.
* No default.

sslAltNameToCheck =  <alternateName1>, <alternateName2>, ...
* Optional. 
* Check the alternate name of the client's certificate against this list 
  of names.
* If there is no match, assume that Splunk is not authenticated against this
  server.
* requireClientCert must be set to true for this setting to work.
* No default.

############################################################################
# Introspection settings
############################################################################

[introspection:generator:disk_objects]
* For 'introspection_generator_addon', packaged with Splunk; provides the
  data ("i-data") consumed, and reported on, by 'introspection_viewer_app'
  (due to ship with a future release).
* This stanza controls the collection of i-data about: indexes; bucket
  superdirectories (homePath, coldPath, ...); volumes; search dispatch
  artifacts.
* On forwarders the collection of index, volumes and dispatch disk objects
  is disabled.

acquireExtra_i_data = true | false
* If true, extra Disk Objects i-data is emitted; you can gain more insight
  into your site, but at the cost of greater resource consumption both
  directly (the collection itself) and indirectly (increased disk and
  bandwidth utilization, to store the produced i-data).
* Please consult documentation for list of regularly emitted Disk Objects
  i-data, and extra Disk Objects i-data, appropriate to your release.
* Default: false

collectionPeriodInSecs = <positive integer>
* Controls frequency of Disk Objects i-data collection; higher frequency
  (hence, smaller period) gives a more accurate picture, but at the cost of
  greater resource consumption both directly (the collection itself) and
  indirectly (increased disk and bandwidth utilization, to store the
  produced i-data).
* Default: 600 (10 minutes)

[introspection:generator:disk_objects__indexes]
  * This stanza controls the collection of i-data about indexes.
  * Inherits the values of 'acquireExtra_i_data' and 'collectionPeriodInSecs'
    attributes from the 'introspection:generator:disk_objects' stanza, but
    may be enabled/disabled independently of it.
  * This stanza should only be used to force collection of i-data about
    indexes on dedicated forwarders.
  * Default: Data collection is disabled on universal forwarders and
    enabled on all other installations.

[introspection:generator:disk_objects__volumes]
  * This stanza controls the collection of i-data about volumes.
  * Inherits the values of 'acquireExtra_i_data' and 'collectionPeriodInSecs'
    attributes from the 'introspection:generator:disk_objects' stanza, but
    may be enabled/disabled independently of it.
  * This stanza should only be used to force collection of i-data about
    volumes on dedicated forwarders.
  * Default: Data collection is disabled on universal forwarders and
    enabled on all other installations.

[introspection:generator:disk_objects__dispatch]
  * This stanza controls the collection of i-data about search dispatch artifacts.
  * Inherits the values of 'acquireExtra_i_data' and 'collectionPeriodInSecs'
    attributes from the 'introspection:generator:disk_objects' stanza, but
    may be enabled/disabled independently of it.
  * This stanza should only be used to force collection of i-data about
    search dispatch artifacts on dedicated forwarders.
  * Default: Data collection is disabled on universal forwarders and
    enabled on all other installations.

[introspection:generator:disk_objects__fishbucket]
* This stanza controls the collection of i-data about:
  $SPLUNK_DB/fishbucket, where we persist per-input status of file-based
  inputs.
* Inherits the values of 'acquireExtra_i_data' and 'collectionPeriodInSecs'
  attributes from the 'introspection:generator:disk_objects' stanza, but may
  be enabled/disabled independently of it.

[introspection:generator:disk_objects__bundle_replication]
* This stanza controls the collection of i-data about:
  bundle replication metrics of distributed search
* Inherits the values of 'acquireExtra_i_data' and 'collectionPeriodInSecs'
  attributes from the 'introspection:generator:disk_objects' stanza, but may
  be enabled/disabled independently of it.

[introspection:generator:disk_objects__partitions]
* This stanza controls the collection of i-data about: disk partition space
  utilization.
* Inherits the values of 'acquireExtra_i_data' and 'collectionPeriodInSecs'
  attributes from the 'introspection:generator:disk_objects' stanza, but may
  be enabled/disabled independently of it.

[introspection:generator:disk_objects__summaries]
* Introspection data about summary disk space usage. Summary disk usage
  includes both data model and report summaries. The usage is collected
  for each summaryId, locally at each indexer.

disabled = true | false
* If not specified, inherits the value from
  [introspection:generator:disk_objects] stanza.

collectionPeriodInSecs = <positive integer>
* Controls frequency, in seconds, of Disk Objects - summaries 
  collection; higher frequency (hence, smaller period) gives a more accurate 
  picture, but at the cost of greater resource consumption directly 
  (the summaries collection itself);
  it is not recommended for a period less than 15 minutes.
* If you enable summary collection, the first collection happens 5 minutes
  after the Splunk instance is started. For every subsequent collection, this
  setting is honored.
* If 'collectionPeriodInSecs' is smaller than 5 * 60, it resets to
  30 minutes internally.
* Set to (N*300) seconds. Any remainder is ignored.
* Default: 1800 (30 minutes)

[introspection:generator:resource_usage]
* For 'introspection_generator_addon', packaged with Splunk; provides the
  data ("i-data") consumed, and reported on, by 'introspection_viewer_app'
  (due to ship with a future release).
* "Resource Usage" here refers to: CPU usage; scheduler overhead; main
  (physical) memory; virtual memory; pager overhead; swap; I/O; process
  creation (a.k.a. forking); file descriptors; TCP sockets; receive/transmit
  networking bandwidth.
* Resource Usage i-data is collected at both hostwide and per-process
  levels; the latter, only for processes associated with this SPLUNK_HOME.
* Per-process i-data for Splunk search processes include additional,
  search-specific, information.

acquireExtra_i_data = true | false
* If set to true, extra Resource Usage i-data is emitted; you can gain 
  more insight into your site, but at the cost of greater resource 
  consumption both directly (the collection itself) and indirectly 
  (increased disk and bandwidth utilization, to store the produced i-data).
* Please consult documentation for list of regularly emitted Resource Usage
  i-data, and extra Resource Usage i-data, appropriate to your release.
* Default: false

collectionPeriodInSecs = <positive integer>
* Controls frequency of Resource Usage i-data collection; higher frequency
  (hence, smaller period) gives a more accurate picture, but at the cost of
  greater resource consumption both directly (the collection itself) and
  indirectly (increased disk and bandwidth utilization, to store the
  produced i-data).
* Default: 600 (10 minutes) on Universal Forwarders, and 10 (1/6th of a minute) 
  on non-Universal Forwarders.

[introspection:generator:resource_usage__iostats]
* This stanza controls the collection of i-data about: IO Statistics data
* "IO Statistics" here refers to: read/write requests; read/write sizes;
  io service time; cpu usage during service
* IO Statistics i-data is sampled over the collectionPeriodInSecs
* Does not inherit the value of the 'collectionPeriodInSecs' attribute from the
  'introspection:generator:resource_usage' stanza, and may be enabled/disabled
  independently of it.

collectionPeriodInSecs = <positive integer>
* Controls interval of IO Statistics i-data collection; higher intervals
  gives a more accurate picture, but at the cost of greater resource consumption
  both directly (the collection itself) and indirectly (increased disk and
  bandwidth utilization, to store the produced i-data).
* Default: 60 (1 minute)

[introspection:generator:kvstore]
* For 'introspection_generator_addon', packaged with Splunk.
* "KV Store" here refers to: statistics information about KV Store process.

serverStatsCollectionPeriodInSecs = <positive integer>
* Controls frequency, in seconds, of KV Store server status collection
* Default: 27

collectionStatsCollectionPeriodInSecs = <positive integer>
* Controls frequency, in seconds, of KV Store db statistics collection.
* Default: 600 (10 minutes)

profilingStatsCollectionPeriodInSecs = <positive integer>
* Controls frequency, in seconds, of KV Store profiling data collection.
* Default: 5 seconds

rsStatsCollectionPeriodInSecs = <positive integer>
* Controls frequency, in seconds, of KV Store replica set stats collectiok
* Default: 60 seconds

############################################################################
# Settings used to control commands started by Splunk
############################################################################

[commands:user_configurable]

prefix = <path>
* All non-internal commands started by splunkd are prefixed with this
  string, allowing for "jailed" command execution.
* Should be only one word.  In other words, commands are supported, but
  commands and arguments are not.
* Applies to commands such as: search scripts, scripted inputs, SSL
  certificate generation scripts.  (Any commands that are
  user-configurable).
* Does not apply to trusted/non-configurable command executions, such as:
  splunk search, splunk-optimize, gunzip.
* No default.


############################################################################
# search head clustering configuration
############################################################################

[shclustering]
disabled = <boolean>
* Disables or enables search head clustering on this instance.
* When enabled, the captain needs to be selected via a
  bootstrap mechanism. Once bootstrapped, further captain
  selections are made via a dynamic election mechanism.
* When enabled, you must also specify the cluster member's own server
  address / management URI for identification purpose. This can be
  done in 2 ways: by specifying the 'mgmt_uri' setting individually on
  each member or by specfing pairs of 'GUID, mgmt-uri' strings in the
  servers_list attribute.
* Default: true

mgmt_uri = [ mgmt-URI ]
* The management URI is used to identify the cluster member's own address to
  itself.
* Either 'mgmt_uri' or 'servers_list' is necessary.
* The 'mgmt_uri' setting is simpler to author but is unique for each member.
* The 'servers_list' setting is more involved, but can be copied as a 
  config string to all members in the cluster.

servers_list = [ <(GUID, mgmt-uri);>+ ]
* A semicolon separated list of instance GUIDs and management URIs.
* Each member uses its GUID to identify its own management URI.

adhoc_searchhead = <boolean>
* This setting configures a member as an adhoc search head; i.e., the member
  does not run any scheduled jobs.
* Use the setting 'captain_is_adhoc_searchhead' to reduce compute load on the
  captain.
* Default: false

no_artifact_replications = <boolean>
* Prevent this Search Head Cluster member to be selected as a target for 
  replications.
* This is an advanced setting, and not to be changed without proper 
  understanding of the implications.
* Default: false

captain_is_adhoc_searchhead = <boolean>
* This setting prohibits the captain from running scheduled jobs.
* The captain is dedicated to controlling the activities of the cluster,
  but can also run adhoc search jobs from clients.
* Default: false

preferred_captain = <boolean>
* The cluster tries to assign captaincy to a member with 
 'preferred_captain=true'.
* Note that it is not always possible to assign captaincy to a member with
  preferred_captain=true - for example, if none of the preferred members is
  reachable over the network. In that case, captaincy might remain on a
  member with preferred_captain=false.
* Default: true

prevent_out_of_sync_captain = <boolean>
* This setting prevents a node that could not sync config changes to current
  captain from becoming the cluster captain.
* This setting takes precedence over the preferred_captain setting. For example,
  if there are one or more preferred captain nodes but the nodes cannot sync config
  changes with the current captain, then the current captain retains captaincy even
  if it is not a preferred captain.
* This must be set to the same value on all members.
* Default: true

replication_factor = <positive integer>
* Determines how many copies of search artifacts are created in the cluster.
* This must be set to the same value on all members.
* Default: 3

pass4SymmKey = <password>
* Secret shared among the members in the search head cluster to prevent any
  arbitrary instance from connecting to the cluster.
* All members must use the same value.
* If set in the [shclustering] stanza, it takes precedence over any setting
  in the [general] stanza.
* Unencrypted passwords must not begin with "$1$", as this is used by
  Splunk software to determine if the password is already encrypted.
* Default: 'changeme' from the [general] stanza in the default the
  server.conf file.

async_replicate_on_proxy = <boolean>
* If the jobs/${sid}/results REST endpoint had to be proxied to a different
  member due to missing local replica, this attribute automatically
  schedules an async replication to that member when set to true.
* Default is true.

master_dump_service_periods = <integer>
* If SHPMaster info is switched on in log.cfg, then captain statistics 
  are dumped in splunkd.log after the specified number of service periods.
  Purely a debugging aid.
* Default: 500

long_running_jobs_poll_period = <integer>
* Long running delegated jobs are polled by the captain every
  "long_running_jobs_poll_period" seconds to ascertain whether they are
  still running, in order to account for potential node/member failure.
* Default: 600 (10 minutes)

scheduling_heuristic = <string>
* This setting configures the job distribution heuristic on the captain.
* There are currently two supported strategies: 'round_robin' or
  'scheduler_load_based'.
* Default: 'scheduler_load_based'

id = <GUID>
* Unique identifier for this cluster as a whole, shared across all cluster
  members.
* By default, Splunk software arranges for a unique value to be generated and
  shared across all members.

cxn_timeout = <integer>
* Low-level timeout, in seconds, for establishing connection between 
  cluster members.
* Default: 60

send_timeout = <integer>
* Low-level timeout, in seconds, for sending data between search head 
  cluster members.
* Default: 60

rcv_timeout = <integer>
* Low-level timeout, in seconds, for receiving data between search head 
  cluster members.
* Default: 60

cxn_timeout_raft = <integer>
* Low-level timeout, in seconds, for establishing connection between search 
  head cluster members for the raft protocol.
* Default: 2

send_timeout_raft = <integer>
* Low-level timeout, in seconds, for sending data between search head 
  cluster members for the raft protocol.
* Default: 5

rcv_timeout_raft = <integer>
* Low-level timeout, in seconds, for receiving data between search head 
  cluster members for the raft protocol.
* Default: 5

rep_cxn_timeout = <integer>
* Low-level timeout, in seconds, for establishing connection for replicating 
  data.
* Default: 5

rep_send_timeout = <integer>
* Low-level timeout, in seconds, for sending replication slice data 
  between cluster members.
* This is a soft timeout. When this timeout is triggered on source peer,
  it tries to determine if target is still alive. If it is still alive,
  it reset the timeout for another rep_send_timeout interval and continues.
  If target has failed or cumulative timeout has exceeded
  rep_max_send_timeout, replication fails.
* Default: 5

rep_rcv_timeout = <integer>
* Low-level timeout, in seconds, for receiving acknowledgement data from 
  members.
* This is a soft timeout. When this timeout is triggered on source member,
  it tries to determine if target is still alive. If it is still alive,
  it reset the timeout for another rep_send_timeout interval and continues.
  If target has failed or cumulative timeout has exceeded
  the 'rep_max_rcv_timeout' setting, replication fails.
* Default: 10

rep_max_send_timeout = <integer>
* Maximum send timeout, in seconds, for sending replication slice data 
  between cluster members.
* On 'rep_send_timeout' source peer determines if total send timeout has
  exceeded rep_max_send_timeout. If so, replication fails.
* If cumulative rep_send_timeout exceeds 'rep_max_send_timeout', replication
  fails.
* Default: 600 (10 minutes)

rep_max_rcv_timeout = <integer>
* Maximum cumulative receive timeout, in seconds, for receiving acknowledgement 
  data from members.
* On 'rep_rcv_timeout' source member determines if total receive timeout has
  exceeded 'rep_max_rcv_timeout'. If so, replication fails.
* Default: 600 (10 minutes)

log_heartbeat_append_entries = <boolean>
* If true, Splunk software logs the the low-level heartbeats between members in
  splunkd_access.log file. These heartbeats are used to maintain the authority
  of the captain authority over other members.
* Default: false.

election_timeout_ms = <positive_integer>
* The amount of time, in milliseconds, that a member waits before 
  trying to become the captain.
* Note that modifying this value can alter the heartbeat period (See
  election_timeout_2_hb_ratio for further details)
* A very low value of election_timeout_ms can lead to unnecessary captain
  elections.
* Default: 60000 (1 minute)

election_timeout_2_hb_ratio = <positive_integer>
* The ratio between the election timeout, set in election_timeout_ms, and
  the raft heartbeat period.
* Raft heartbeat period = election_timeout_ms / election_timeout_2_hb_ratio
* A typical ratio between 5 - 20 is desirable. Default is 12 to keep the
  raft heartbeat period at 5s, i.e election_timeout_ms(60000ms) / 12
* This ratio determines the number of heartbeat attempts that would fail
  before a member starts to timeout and tries to become the captain.

heartbeat_timeout = <positive integer>
* The amount of time, in seconds, that the captain considers a member down. 
  After a member is down, the captain initiates fixup steps to replicate
  artifacts from the dead member to its peers.
* This heartbeat exchanges data between the captain and members, which helps in
  maintaining the in-memory centralized state for all the cluster members.
* Note that this heartbeat is different from the Raft heartbeat described
  in the 'election_timeout_2_hb_ratio' setting.
* Default: 60 (1 minute)

raft_rpc_backoff_time_ms = <positive integer>
* Provides a delay, in milliseconds, should a raft RPC request fail.
* This avoids rapid connection requests being made to unreachable peers.
* This setting should not normally be changed from the default.
* Default: 5000 (5 seconds)

access_logging_for_heartbeats = <boolean>
* Only valid on captain
* Enables/disables logging to the splunkd_access.log file for member heartbeats
* NOTE: you do not have to restart captain to set this config parameter.
  Simply run the cli command on master:
  % splunk edit shcluster-config -access_logging_for_heartbeats <<boolean>>
* Default: false (logging disabled)

restart_timeout = <positive integer>
* This is the amount of time the captain waits for a member to come
  back when the instance is restarted (to avoid the overhead of
  trying to fixup the artifacts that were on the peer).

quiet_period = <positive integer>
* Determines the amount of time, in seconds, for which a newly 
  elected captain waits for members to join. During this period the
  captain does not initiate any fixups but instead waits for the
  members to register themselves. Job scheduling and conf
  replication still happen as usual during this time. At the end
  of this time period, the captain builds its view of the cluster
  based on the registered peers and starts normal
  processing.
* Default: 60

max_peer_rep_load = <integer>
* This is the maximum number of concurrent replications that a
  member can take part in as a target.
* Default: 5

target_wait_time = <positive integer>
* Specifies the time, in seconds, that the captain waits for the target 
  of a replication to register itself before it services the artifact again 
  and potentially schedules another fixup.
* Default: 150

manual_detention = on|off
* This property toggles manual detention on member.
* When a node is in manual detention, it does not accept new search jobs,
  including both scheduled and ad-hoc searches. It also does not receive
  replicated search artifacts from other nodes.
* Default: off

percent_peers_to_restart = <integer>
* The percentage of members to restart at one time during rolling restarts.
* Actual percentage may vary due to lack of granularity for smaller peer
  sets regardless of setting, a minimum of 1 peer is restarted per
  round.
* Valid values are between 0 and 100.
* CAUTION: Do not set this attribute to a value greater than 20%. 
  Otherwise, issues can arise during the captain election process.

rolling_restart_with_captaincy_exchange = <boolean>
* If this boolean is turned on, captain tries to exchange captaincy 
  with another node during rolling restart.
* If set to false, captain restarts and captaincy transfers to some 
  other node.
* Default: true

rolling_restart = restart|searchable|searchable_force
* Determines the rolling restart mode for a search head cluster.
* If set to restart, a rolling restart runs in classic mode.
* If set to searchable, a rolling restart runs in searchable (minimal 
  search disruption) mode.
* If set to searchable_force, the search head cluster performs a 
  searchable rolling restart, but overrides the health check
* Note: You do not have to restart any search head members to set this 
  parameter.
  Run this CLI command from any member:
  % splunk edit shcluster-config -rolling_restart 
    restart|searchable|searchable_force
* Default: restart (runs in classic rolling-restart mode)

decommission_search_jobs_wait_secs = <positive integer>
* The amount of time, in seconds, that a search head cluster member waits for
  existing searches to complete before restarting.
* Applies only when rolling restart is triggered in searchable or 
  searchable_force mode
  (i.e.'rolling_restart' is set to "searchable" or "searchable_force").
* Note: You do not have to restart search head members to set this parameter.
  Run this CLI command from any member:
  % splunk edit shcluster-config -decommission_search_jobs_wait_secs 
    <positive integer>
* Default: 180

register_replication_address = <IP address ormachine/domain name>
* This setting is the address on which a member is available for 
  accepting replication data. This is useful in the cases where a member 
  host machine has multiple interfaces and only one of them can be reached 
  by another splunkd instance.
* Can be an IP address, or fully qualified machine/domain name.

executor_workers = <positive integer>
* Number of threads that can be used by the search head clustering
  threadpool.
* A value of 0 is interpreted as 1.
* Default: 10

heartbeat_period = <non-zero positive integer>
* Controls the frequency, in seconds, with which the member attempts 
  to send heartbeats to the captain.
* This heartbeat exchanges data between the captain and members, which 
  helps in maintaining the in-memory centralized state for all the 
  cluster members.
* Note that this heartbeat period is different from the Raft heartbeat 
  period in the election_timeout_2_hb_ratio setting.
* Default: 5

enableS2SHeartbeat = <boolean>
* Splunk software monitors each replication connection for presence of
  a heartbeat. 
* If the heartbeat is not seen for s2sHeartbeatTimeout seconds, it closes 
  the connection.
* Default: true

s2sHeartbeatTimeout = <integer>
* This specifies the global timeout, in seconds, value for monitoring 
  heartbeats on replication connections.
* Splunk software closes a replication connection if a heartbeat is not seen
  for 's2sHeartbeatTimeout' seconds.
* Replication source sends a heartbeat every 30 seconds.
* Default: 600 (10 minutes)

captain_uri = [ static-captain-URI ]
* The management URI of static captain is used to identify the cluster 
  captain for a static captain.

election = <boolean>
* This is used to classify a cluster as static or dynamic (RAFT based).
* If set to false, a static captain, which is used for DR situation.
* If set to true, a dynamic captain election enabled through RAFT protocol.

mode = <member>
* Accepted values are captain and member, mode is used to identify 
  the function of a node in static search head cluster. Setting mode 
  as captain assumes it to function as both captain and a member.

#proxying related
sid_proxying = <boolean>
* Enable or disable search artifact proxying. 
* Changing this affects the proxying of search results, and jobs feed
  is not cluster-aware.
* Only for internal/expert use.
* Default: true

ss_proxying = <boolean>
* Enable or disable saved search proxying to captain.
* Changing this affects the behavior of Searches and Reports page
  in Splunk Web.
* Only for internal/expert use.
* Default: true

ra_proxying = <boolean>
* Enable or disable saved report acceleration summaries proxying to captain.
* Changing this affects the behavior of report acceleration summaries
  page.
* Only for internal/expert use.
* Default: true

alert_proxying = <boolean>
* Enable or disable alerts proxying to captain.
* Changing this impacts the behavior of alerts, and essentially make them
  not cluster-aware.
* Only for internal/expert use.
* Default: true

csv_journal_rows_per_hb = <integer>
* Controls how many rows of CSV from the delta-journal are sent per hb
* Used for both alerts and suppressions
* Do not alter this value without contacting Splunk Support.
* Default: 10000

conf_replication_period = <integer>
* Controls how often, in seconds, a cluster member replicates 
  configuration changes.
* A value of 0 disables automatic replication of configuration changes.
* Default: 5
                                    
conf_replication_max_pull_count = <integer>
* Controls the maximum number of configuration changes a member
  replicates from the captain at one time.
* A value of 0 disables any size limits.
* Default: 1000

conf_replication_max_push_count = <integer>
* Controls the maximum number of configuration changes a member
  replicates to the captain at one time.
* A value of 0 disables any size limits.
* Default: 100

conf_replication_max_json_value_size = [<integer>|<integer>[KB|MB|GB]]
* Controls the maximum size of a JSON string element at any nested
  level while parsing a configuration change from JSON representation.
* If a knowledge object created on a member has some string element
  that exceeds this limit, the knowledge object is not replicated
  to the rest of the search head cluster, and a warning that mentions
  conf_replication_max_json_value_size is written to splunkd.log.
* If you do not specify a unit for the value, the unit defaults to bytes.
* The lower limit of this setting is 512KB.
* When increasing this setting beyond the default, you must take into
  account the available system memory.
* Default: 15MB

conf_replication_include.<conf_file_name> = <boolean>
* Controls whether Splunk replicates changes to a particular type of *.conf
  file, along with any associated permissions in *.meta files.
* Default: false

conf_replication_summary.whitelist.<name> = <whitelist_pattern>
* Whitelist files to be included in configuration replication summaries.

conf_replication_summary.blacklist.<name> = <blacklist_pattern>
* Blacklist files to be excluded from configuration replication summaries.

conf_replication_summary.concerning_file_size = <integer>
* Any individual file within a configuration replication summary that is
  larger than this value (in MB) triggers a splunkd.log warning message.
* Default: 50

conf_replication_summary.period = <timespan>
* Controls how often configuration replication summaries are created.
* Default: 1m (1 minute)

conf_replication_purge.eligibile_count = <integer>
* Controls how many configuration changes must be present before any become
  eligible for purging.
* In other words: controls the minimum number of configuration changes
  Splunk software remembers for replication purposes.
* Default: 20000

conf_replication_purge.eligibile_age = <timespan>
* Controls how old a configuration change must be before it is eligible for
  purging.
* Default: '1d' (1 day).

conf_replication_purge.period = <timespan>
* Controls how often configuration changes are purged.
* Default: 1h (1 hour)

conf_replication_find_baseline.use_bloomfilter_only = <boolean>
* Controls whether or not a search head cluster only uses bloom filters to
  determine a baseline, when it replicates configurations.
* Set to true to only use bloom filters in baseline determination during
  configuration replication.
* Set to false to first attempt a standard method, where the search head
  cluster captain interacts with members to determine the baseline, before
  falling back to using bloom filters.
* Default: false

conf_deploy_repository = <path>
* Full path to directory containing configurations to deploy to cluster
  members.

conf_deploy_staging = <path>
* Full path to directory where preprocessed configurations may be written
  before being deployed cluster members.

conf_deploy_concerning_file_size = <integer>
* Any individual file within <conf_deploy_repository> that is larger than
  this value (in MB) triggers a splunkd.log warning message.
* Default: 50

conf_deploy_fetch_url = <URL>
* Specifies the location of the deployer from which members fetch the
  configuration bundle.
* This value must be set to a <URL> in order for the configuration bundle to
  be fetched.
* No default.

conf_deploy_fetch_mode = auto|replace|none
* Controls configuration bundle fetching behavior when the member starts up.
* When set to "replace", a member checks for a new configuration bundle on
  every startup.
* When set to "none", a member does not fetch the configuration bundle on
  startup.
* Regarding "auto":
  * If no configuration bundle has yet been fetched, "auto" is equivalent
    to "replace".
  * If the configuration bundle has already been fetched, "auto" is
    equivalent to "none".
* Default: replace

artifact_status_fields = <field> ...
* Give a comma separated fields to pick up values from status.csv and 
  info.csv for each search artifact.
* These fields are shown in the CLI/REST endpoint splunk list 
  shcluster-member-artifacts
* Default: user, app, label

encrypt_fields = <field> ...
* These are the fields that need to be re-encrypted when a Search Head 
  Cluster does its own first time run on syncing all members with a new s
  plunk.secret key 
* Give a comma separated fields as a triple elements 
  <conf-file>:<stanza-prefix>:<key elem>
* For matching all stanzas from a conf, leave the stanza-prefix 
  empty. For example: "server: :pass4SymmKey" matches all stanzas 
  with pass4SymmKey as key in server.conf
* Default: storage/passwords, secret key for clustering/shclustering,
  server ssl config 

enable_jobs_data_lite = <boolean> 
*This is for memory reduction on the captain for Search head clustering, 
  leads to lower memory in captain while slaves send the artifacts 
  status.csv as a string. 
* Default: false

shcluster_label = <string>
* This specifies the label of the search head cluster.

retry_autosummarize_or_data_model_acceleration_jobs = <boolean>
* Controls whether the captain tries a second time to delegate an
  auto-summarized or data model acceleration job, if the first attempt to
  delegate the job fails.
* Default: true

[replication_port://<port>]
############################################################################
# Configures the member to listen on a given TCP port for replicated data
# from another cluster member.
# At least one replication_port must be configured and not disabled.
############################################################################

disabled = <boolean>
* Set to true to disable this replication port stanza.
* Default: false

listenOnIPv6 = no|yes|only
* Toggle whether this listening port listens on IPv4, IPv6, or both.
* If not present, the setting in the [general] stanza is used.

acceptFrom = <network_acl> ...
* Lists a set of networks or addresses from which to accept connections.
* This setting only takes effect when 'appServerPorts' is set to a
  non-zero value.
* Separate multiple rules with commas or spaces.
* Each rule can be in one of the following formats:
    1. A single IPv4 or IPv6 address (examples: "10.1.2.3", "fe80::4a3")
    2. A Classless Inter-Domain Routing (CIDR) block of addresses
       (examples: "10/8", "192.168.1/24", "fe80:1234/32")
    3. A DNS name, possibly with a "*" used as a wildcard
       (examples: "myhost.example.com", "*.splunk.com")
    4. "*", which matches anything
* You can also prefix an entry with '!' to cause the rule to reject the
  connection. The input applies rules in order, and uses the first one that
  matches.
  For example, "!10.1/16, *" allows connections from everywhere except
  the 10.1.*.* network.
* Default: "*" (accept from anywhere)

[replication_port-ssl://<port>]
* This configuration is the same as the replication_port stanza, but uses SSL.

disabled = true|false
* Set to true to disable this replication port stanza.
* Default: false

listenOnIPv6 = no|yes|only
* Toggle whether this listening port listens on IPv4, IPv6, or both.
* If not present, the setting in the [general] stanza is used.

acceptFrom = <network_acl> ...
* This setting is the same as the setting in the [replication_port] stanza. 

serverCert = <path>
* Full path to file containing private key and server certificate.
* The <path> must refer to a PEM format file.
* No default.

sslPassword = <password>
* Server certificate password, if any.
* No default.

password = <password>
* DEPRECATED; use 'sslPassword' instead.
* Used only if 'sslPassword' is not set.

rootCA = <path>
* DEPRECATED; use '[sslConfig]/sslRootCAPath' instead.
* Used only if '[sslConfig]/sslRootCAPath' is not set.
* Full path to the root CA (Certificate Authority) certificate store.
* The <path> must refer to a PEM format file containing one or more root CA
  certificates concatenated together.
* No default.

cipherSuite = <cipher suite string>
* If set, uses the specified cipher string for the SSL connection.
* If not set, uses the default cipher string.
* provided by OpenSSL.  This is used to ensure that the server does not
  accept connections using weak encryption protocols.

supportSSLV3Only = <boolean>
* DEPRECATED.  SSLv2 is now always disabled.  The exact set of SSL versions
  allowed is now configurable via the "sslVersions" setting above.

useSSLCompression = <boolean>
* If true, enables SSL compression.
* Default: true

compressed = <boolean>
* DEPRECATED; use 'useSSLCompression' instead.
* Used only if 'useSSLCompression' is not set.

requireClientCert = <boolean>
* Requires that any peer that connects to replication port has a certificate
  that can be validated by certificate authority specified in rootCA.
* Default: false

allowSslRenegotiation = <boolean>
* In the SSL protocol, a client may request renegotiation of the connection
  settings from time to time.
* Setting this to false causes the server to reject all renegotiation
  attempts, breaking the connection.  This limits the amount of CPU a
  single TCP connection can use, but it can cause connectivity problems
  especially for long-lived connections.
* Default: true

############################################################################
# KV Store configuration
############################################################################
[kvstore]

disabled = <boolean>
* Set to true to disable the KV Store process on the current server. To
  completely disable KV Store in a deployment with search head clustering or
  search head pooling, you must also disable KV Store on each individual
  server.
* Default: false

port = <port>
* Port to connect to the KV Store server.
* Default: 8191

replicaset = <replset>
* Replicaset name.
* Default: splunkrs

distributedLookupTimeout = <seconds>
* This setting has been removed, as it is no longer needed.

shutdownTimeout = <integer>
* Time, in seconds, to wait for a clean shutdown of the KV Store. If this time
  is reached after signaling for a shutdown, KV Store is forcibly terminated
* Default: 100

initAttempts = <integer>
* The maximum number of attempts to initialize the KV Store when starting
  splunkd.
* Default: 300

replication_host = <host>
* The host name to access the KV Store.
* This setting has no effect on a single Splunk instance.
* When using search head clustering, if the "replication_host" value is not
  set in the [kvstore] stanza, the host you specify for
  "mgmt_uri" in the [shclustering] stanza is used for KV
  Store connection strings and replication.
* In search head pooling, this host value is a requirement for using KV
  Store.
* This is the address on which a kvstore is available for accepting
  remotely.

verbose = <boolean>
* Set to true to enable verbose logging.
* Default: false

verboseLevel = <nonnegative integer>
* When verbose logging is enabled specify verbose level for logging
  from 0 to 5, where 5 is the most verbose.
* Default: 2

dbPath = <path>
* Path where KV Store data is stored.
* Changing this directory after initial startup does not move existing data.
  The contents of the directory should be manually moved to the new
  location.
* Default: $SPLUNK_DB/kvstore

oplogSize = <integer>
* The size of the replication operation log, in MB, for environments
  with search head clustering or search head pooling.
  In a standalone environment, 20% of this size is used.
* After the KV Store has created the oplog for the first time, changing this
  setting does NOT affect the size of the oplog. A full backup and restart
  of the KV Store is required.
* Do not change this setting without first consulting with Splunk Support.
* Default: 1000MB (1GB)

replicationWriteTimeout = <integer>
* The time to wait, in seconds, for replication to complete while saving KV store
  operations. When the value is 0, the process never times out.
* Used for replication environments (search head clustering or search
  head pooling).
* Default: 1800 (30 minutes)

caCertFile = <path>
* DEPRECATED; use '[sslConfig]/sslRootCAPath' instead.
* Used only if 'sslRootCAPath' is not set.
* Full path to a CA (Certificate Authority) certificate(s) PEM format file.
* If specified, it is used in KV Store SSL connections and
  authentication.
* Only used when Common Criteria is enabled (SPLUNK_COMMON_CRITERIA=1)
  or FIPS is enabled (i.e. SPLUNK_FIPS=1).
* NOTE: Splunk plans to submit Splunk Enterprise for Common Criteria
  evaluation. Splunk does not support using the product in Common
  Criteria mode until it has been certified by NIAP. See the "Securing
  Splunk Enterprise" manual for information on the status of Common
  Criteria certification.
* Default: $SPLUNK_HOME/etc/auth/cacert.pem

caCertPath = <filepath>
* DEPRECATED; use '[sslConfig]/sslRootCAPath' instead.

serverCert = <filepath>
* A certificate file signed by the signing authority specified above by
  caCertPath.
* In search head clustering or search head pooling, the certificates at
  different members must share the same ‘subject'.
* The Distinguished Name (DN) found in the certificate’s subject, must
  specify a non-empty value for at least one of the following attributes:
  Organization (O), the Organizational Unit (OU) or the
  Domain Component (DC).
* Only used when Common Criteria is enabled (SPLUNK_COMMON_CRITERIA=1)
  or FIPS is enabled (i.e. SPLUNK_FIPS=1).
* NOTE: Splunk plans to submit Splunk Enterprise for Common Criteria
  evaluation. Splunk does not support using the product in Common
  Criteria mode until it has been certified by NIAP. See the "Securing
  Splunk Enterprise" manual for information on the status of Common
  Criteria certification.

sslKeysPath = <filepath>
* DEPRECATED; use 'serverCert' instead.
* Used only when 'serverCert' is empty.

sslPassword = <password>
* Password of the private key in the file specified by 'serverCert' above.
* Must be specified if FIPS is enabled (i.e. SPLUNK_FIPS=1), otherwise, KV
  Store is not available.
* Only used when Common Criteria is enabled (SPLUNK_COMMON_CRITERIA=1)
  or FIPS is enabled (i.e. SPLUNK_FIPS=1).
* NOTE: Splunk plans to submit Splunk Enterprise for Common Criteria
  evaluation. Splunk does not support using the product in Common
  Criteria mode until it has been certified by NIAP. See the "Securing
  Splunk Enterprise" manual for information on the status of Common
  Criteria certification.
* No default.

sslKeysPassword = <password>
* DEPRECATED; use 'sslPassword' instead.
* Used only when 'sslPassword' is empty.

sslCRLPath = <filepath>
* Certificate Revocation List file.
* Optional. Defaults to no Revocation List.
* Only used when Common Criteria is enabled (SPLUNK_COMMON_CRITERIA=1)
  or FIPS is enabled (i.e. SPLUNK_FIPS=1).
* NOTE: Splunk plans to submit Splunk Enterprise for Common Criteria
  evaluation. Splunk does not support using the product in Common
  Criteria mode until it has been certified by NIAP. See the "Securing
  Splunk Enterprise" manual for information on the status of Common
  Criteria certification.

modificationsReadIntervalMillisec = <integer>
* Specifies how often, in milliseconds, to check for modifications to 
  KV Store collections in order to replicate changes for distributed 
  searches.
* Default: 1000 (1 second)

modificationsMaxReadSec = <integer>
* Maximum time interval KVStore can spend while checking for modifications
  before it produces collection dumps for distributed searches.
* Default: 30

[indexer_discovery]
pass4SymmKey = <password>
* Security key shared between master node and forwarders.
* If specified here, the same value must also be specified on all forwarders
  connecting to this master.
* Unencrypted passwords must not begin with "$1$", as this is used by
  Splunk software to determine if the password is already encrypted.

polling_rate = <integer>
* A value between 1 to 10. This value affects the forwarder polling 
  frequency to achieve the desired polling rate. The number of connected 
  forwarders is also taken into consideration.
* The formula used to determine effective polling interval, 
  in Milliseconds, is:
  (number_of_forwarders/polling_rate + 30 seconds) * 1000
* Default: 10

indexerWeightByDiskCapacity = <boolean>
* If set to true, it instructs the forwarders to use weighted load 
  balancing. In weighted load balancing, load balancing is based on the 
  total disk capacity  of the target indexers, with the forwarder streaming 
  more data to indexers with larger disks.
*  The traffic sent to each indexer is based on the ratio of:
   indexer_disk_capacity/total_disk_capacity_of_indexers_combined
* Default: false

############################################################################
# Node level authentication
############################################################################
[node_auth]
signatureVersion = <comma-separated list>
* A list of authentication protocol versions that nodes of a Splunk
  deployment use to authenticate to other nodes.
* Each version of node authentication protocol implements an algorithm
  that specifies cryptographic parameters to generate authentication data.
* Nodes may only communicate using the same authentication protocol version.
* For example, if you set "signatureVersion = v1,v2" on one node, that
  node sends and accepts authentication data using versions "v1" and "v2"
  of the protocol, and you must also set "signatureVersion" to one of
  "v1", "v2", or "v1,v2" on other nodes for those nodes to mutually
  authenticate.
* For higher levels of security, set 'signatureVersion' to "v2".
* Default: v1,v2

############################################################################
# Cache Manager Configuration
############################################################################
[cachemanager]
max_concurrent_downloads = <unsigned integer>
* The maximum number of buckets that can be downloaded simultaneously from
  external storage
* Default: 8

max_concurrent_uploads = <unsigned integer>
* The maximum number of buckets that can be uploaded simultaneously to external
  storage.
* Default: 8

eviction_policy = <string>
* The name of the eviction policy to use.
* Current options: lru, clock, random, lrlt, noevict
* Do not change the value from the default unless instructed by
  Splunk Support.
* Default: lru

enable_eviction_priorities = <boolean>
* When requesting buckets, search peers can give hints to the Cache Manager
  about the relative importance of buckets.
* When enabled, the Cache Manager takes the hints into consideration; when
  disabled, hints are ignored.
* Default: true

eviction_padding = <positive integer>
* Specifies the additional space, in megabytes, beyond 'minFreeSpace' that the
  cache manager uses as the threshold to start evicting data.
* If free space on a partition falls below ('minFreeSpace' + 'eviction_padding'),
  then the cache manager tries to evict data from remote storage enabled indexes.
* Default: 5120 (~5GB)

max_cache_size = <positive integer>
* Specifies the maximum space, in megabytes, per partition, that the cache can
  occupy on disk. If this value is exceeded, the cache manager starts evicting buckets.
* A value of 0 means this feature is not used, and has no maximum size.
* Default: 0

hotlist_recency_secs = <unsigned integer>
* The cache manager attempts to defer bucket eviction until the interval
  between the bucket's latest time and the current time exceeds this setting,
  in seconds.
* This setting can be overridden on a per-index basis in indexes.conf.
* Default: 86400 (24 hours)

hotlist_bloom_filter_recency_hours = <unsigned integer>
* The cache manager attempts to defer eviction of the non-journal and non-tsidx
  bucket files, such as the bloomfilter file, until the interval between the
  bucket's latest time and the current time exceeds this setting.
* This setting can be overridden on a per-index basis in indexes.conf.
* Default: 360 (15 days)

# Raft Statemachine configuration
############################################################################
[raft_statemachine]

disabled = <boolean>
* Set to true to disable the raft statemachine.
* This feature require search head clustering to be enabled.
* Any consensus replication among search heads use this feature.
* Default: true

replicate_search_peers = <boolean>
* Add/remove search-server request is applied on all members
  of a search head cluster, when this value to set to true.
* Require a healthy search head cluster with a captain.

[watchdog]
disabled = true|false
* Disables thread monitoring functionality. 
* Any thread that has been blocked for more than 'responseTimeout' milliseconds
  is logged to $SPLUNK_HOME/var/log/watchdog/watchdog.log
* Defaults to false.

responseTimeout = <decimal>
* Maximum time, in seconds, that a thread can take to respond before the 
  watchdog logs a 'thread blocked' incident.
* The minimum value for 'responseTimeout' is 0.1. 
* If you set 'responseTimeout' to lower than 0.1, the setting uses the minimum 
  value instead.
* Defaults to 8 seconds.

actions = <actions_list>
* A comma-separated list of actions that execute sequentially when a blocked 
  thread is encountered.
* Currently, the only available actions are 'pstacks', 'script' and 'bulletin'.
* 'pstacks' enables call stack generation for a blocked thread.
* Call stack generation gives the user immediate information on the potential 
  bottleneck or deadlock.
* The watchdog saves each call stack in a separate file in 
  $SPLUNK_HOME/var/log/watchdog with the following file name format: 
  wd_stack_<pid>_<thread_name>_%Y_%m_%d_%H_%M_%S.%f_<uid>.log.
* 'script' executes specified script.
* 'bulletin' shows a message on the web interface.
* NOTE: This setting should be used only during troubleshooting, and if you have 
  been asked to set it by a Splunk Support engineer. It might degrade performance
  by increasing CPU and disk usage.
* Defaults to empty list (no action executed).

actionsInterval = <decimal>
* The timeout, in seconds, that the watchdog uses while tracing a blocked 
  thread. The watchdog executes each action every 'actionsInterval' seconds.
* The minimum value for 'actionsInterval' is 0.01. 
* If you set 'actionsInterval' to lower than 0.01, the setting uses the minimum 
  value instead.
* NOTE: Very small timeout may have impact performance by increasing CPU usage.
  Splunk may be also slowed down by frequently executed action.
* Defaults to 0.7 second.

pstacksEndpoint = <boolean>
* Enables pstacks endpoint at /services/server/pstacks
* Endpoint allows ad-hoc pstacks generation of all running threads.
* NOTE: This setting is ignored if 'watchdog' is not enabled.
* NOTE: This setting should be used only during troubleshooting and only if you 
  have been explicitly asked to set it by a Splunk Support engineer. 
* Defaults to true.

[watchdog:timeouts]
reaperThread = <decimal>
* Maximum time, in seconds, that a reaper thread can take to respond before the 
  watchdog logs a 'thread blocked' incident.
* The minimum value for 'reaperThread' is 0.1. 
* If you set 'reaperThread' to lower than 0.1, the setting uses the minimum 
  value instead.
* This value is used only for threads dedicated to clean up dispatch directories 
  and search artifacts.
* Defaults to 30 seconds.

[watchdogaction:pstacks]
dumpAllThreads = <boolean>
* Determines whether or not the watchdog saves stacks of all monitored threads 
  when it encounters a blocked thread.
* If you set 'dumpAllThreads' to true, the watchdog generates call stacks for 
  all threads, regardless of thread state.
* NOTE: This setting is ignored if 'pstacks' is not enabled in the 'actions' 
  list.
* NOTE: This setting should be used only during troubleshooting, and if you have 
  been asked to set it by a Splunk Support engineer. It may impact performance
  by increasing CPU and disk usage.
* Defaults to false.

stacksBufferSizeOrder = <unsigned integer>
* Controls the maximum number of call stacks an internal queue can hold.
* The watchdog uses the internal queue to temporarily store a call stack between 
  the time the watchdog generates the call stack and the time it saves the call 
  stack to a file.
* Increase the value of this setting if you see gaps in stack files due to high 
  frequency of call stack generation. This might occur when, for example, you 
  set 'stacksBufferSizeOrder' to a very low value, or if the number of threads is 
  high.
* This number must be in the range 1 to 16.
* The watchdog uses this value to calculate the real size of the buffer, whose 
  value must be a power of 2. For example, if 'stackBufferSizeOrder' is 4, the 
  size of the buffer is 4 ^ 2, or 16.
* This setting is ignored if 'pstacks' is not enabled in the 'actions' list.
* CAUTION: Setting to too low a value can cause dropped call stacks, and too high 
  a value can cause increased memory consumption.
* Defaults to 14.

maxStacksPerBlock = <unsigned integer>
* Maximum number of stacks that the watchdog can generate for a blocked thread.
* If you set 'dumpAllThreads' to true, the watchdog generates call stacks for 
  all threads.
* If the blocked thread starts responding again, the count of stacks that the 
  watchdog has generated resets to zero.
* If another thread blockage occurs, the watchdog begins generating stacks 
  again, up to 'maxStacksPerBlock' stacks.
* When set to 0, an unlimited number of stacks will be generated.
* NOTE: This setting is ignored if 'pstacks' is not enabled in the 'actions' 
  list.
* Defaults to 100.

[watchdogaction:script]
path = <string>
* The path to the script to execute when the watchdog triggers the action.
* No default. If you do not set 'path', the watchdog ignores the action.

useShell = <boolean>
* If set to true, the script runs from the OS shell
  ("/bin/sh -c" on UNIX, "cmd.exe /c" on Windows)
* If set to false, the program will be run directly without attempting to
  expand shell metacharacters.
* Defaults to false.

forceStop = <boolean>
* Whether or not the watchdog forcefully stops an active watchdog action script
  when a blocked thread starts to respond.
* Use this setting when, for example, the watchdog script has internal logic that 
  controls its lifetime and must run without interruption.
* Defaults to false.

forceStopOnShutdown = <boolean>
* If you set this setting to "true", the watchdog forcefully stops active watchdog 
  scripts upon receipt of a shutdown request.
* Defaults to true.

############################################################################
# Parallel Reduce Configuration
############################################################################
[parallelreduce]
pass4SymmKey = <password>
* Security key shared between reducers and regular indexers.
* The same value must also be specified on all intermediaries.
* Unencrypted passwords must not begin with "$1$", as this is used by
  Splunk software to determine if the password is already encrypted.



@
@[rendezvous_service]
@
@uri = <uri>
@* Points to the tenant rendezvous service.
@* If empty or unspecified, disables rendezvous service heartbeats.
@* Currently, only HTTP is supported by the service.
@* Optional
@* Example <uri> : <scheme>://<hostname>:<port>/<tenantId>/<rendezvous_path>
@
@refresh_interval = <positive integer>
@* Frequency, in seconds, at which the rendezvous service is updated.
@* Optional
@* Default: 30


@
@[bucket_catalog_service]
@
@uri = <uri>
@* Points to the tenant bucket catalog service.
@* Required.
@* Currently, only HTTP is supported by the service.
@* Example: <scheme>://<hostname>:<port>/<tenantId>/<bucket_catalog_path>
@
@token = <token>

@* Specifies the bearer token that needs to be passed to the bucket 
  catalog service.
@* Optional.
@* Default: bcs_default_token

############################################################################
# Remote Storage of Search Artifacts Configuration
############################################################################
[search_artifact_remote_storage]
disabled = <boolean>
* Currently not supported. This setting is related to a feature that is
  still under development.
* Optional.
* Specifies whether or not search artifacts should be stored remotely.
* Splunkd does not clean up artifacts from remote storage. Set up cleanup
  separately with the remote storage provider.
* Default: true

path = <path on server>
* The path attribute points to the remote storage location where artifacts reside.
* The format for this attribute is: <scheme>://<remote-location-specifier>
  * The "scheme" identifies a supported external storage system type.
  * The "remote-location-specifier" is an external system-specific string for
     identifying a location inside the storage system.
* These external systems are supported:
  * Object stores that support AWS's S3 protocol. These use the scheme "s3".
    For example, "path=s3://mybucket/some/path".
* This is a required setting. If you do not set the path, the search artifact
  remote storage feature is disabled.
* No default.

############################################################################
# S3 specific settings
############################################################################

remote.s3.header.<http-method-name>.<header-field-name> = <String>
* Optional.
* Enable server-specific features, such as reduced redundancy, encryption, 
  and so on, by passing extra HTTP headers with the REST requests.
* The <http-method-name> can be any valid HTTP method. For example, GET, 
  PUT, or ALL, for setting the header field for all HTTP methods.
* Example: remote.s3.header.PUT.x-amz-storage-class = REDUCED_REDUNDANCY

remote.s3.access_key = <String>
* Optional.
* Specifies the access key to use when authenticating with the remote storage
  system supporting the S3 API.
* If not specified, the indexer looks for these environment variables:
  AWS_ACCESS_KEY_ID or AWS_ACCESS_KEY (in that order).
* If the environment variables are not set and the indexer is running on EC2,
  the indexer attempts to use the access key from the IAM role.
* No default.

remote.s3.secret_key = <String>
* Optional.
* Specifies the secret key to use when authenticating with the remote storage
  system supporting the S3 API.
* If not specified, the indexer looks for these environment variables:
  AWS_SECRET_ACCESS_KEY or AWS_SECRET_KEY (in that order).
* If the environment variables are not set and the indexer is running on EC2,
  the indexer attempts to use the secret key from the IAM role.
* No default.

remote.s3.list_objects_version = v1|v2
* The AWS S3 Get Bucket (List Objects) Version to use.
* See AWS S3 documentation "GET Bucket (List Objects) Version 2" for details.
* Default: v1

remote.s3.signature_version = v2|v4
* Optional.
* The signature version to use when authenticating with the remote storage
  system supporting the S3 API.
* For 'sse-kms' server-side encryption scheme, you must use
  signature_version=v4.
* Default: v4

remote.s3.auth_region = <String>
* Optional
* The authentication region to use for signing requests when interacting with the remote
  storage system supporting the S3 API. 
* Used with v4 signatures only.
* If unset and the endpoint (either automatically constructed or explicitly set with 
  remote.s3.endpoint setting) uses an AWS URL (for example, https://s3-us-west-1.amazonaws.com),
  the instance attempts to extract the value from the endpoint URL (for
  example, "us-west-1").  See the description for the remote.s3.endpoint setting.
* If unset and an authentication region cannot be determined, the request will be signed
  with an empty region value.
* No default.

remote.s3.use_delimiter = true | false
* Optional.
* Specifies whether a delimiter (currently "guidSplunk") should be
  used to list the objects that are present on the remote storage.
* A delimiter groups objects that have the same delimiter value
  so that the listing process can be more efficient as it
  does not need to report similar objects.
* Default: true

remote.s3.supports_versioning = true | false
* Optional.
* Specifies whether the remote storage supports versioning.
* Versioning is a means of keeping multiple variants of an object
  in the same bucket on the remote storage.
* Default: true

remote.s3.endpoint = <URL>
* Optional.
* The URL of the remote storage system supporting the S3 API.
* The scheme, http or https, can be used to enable or disable SSL connectivity
  with the endpoint.
* If not specified and the indexer is running on EC2, the endpoint is
  constructed automatically based on the EC2 region of the instance where the
  indexer is running, as follows: https://s3-<region>.amazonaws.com
* Example: https://s3-us-west-2.amazonaws.com

remote.s3.multipart_download.part_size = <unsigned integer>
* Optional.
* Sets the download size of parts during a multipart download.
* This setting uses HTTP/1.1 Range Requests (RFC 7233) to improve throughput
  overall and for retransmission of failed transfers.
* A value of 0 disables downloading in multiple parts, i.e., files are always
  downloaded as a single (large) part.
* Do not change this value unless that value has been proven to improve
  throughput.
* Minimum value: 5242880 (5 MB)
* Default: 134217728 (128 MB)

remote.s3.multipart_upload.part_size = <unsigned integer>
* Optional.
* Sets the upload size of parts during a multipart upload.
* Minimum value: 5242880 (5 MB)
* Default: 134217728 (128 MB)

remote.s3.multipart_max_connections = <unsigned integer>
* Specifies the maximum number of HTTP connections to have in progress for
  either multipart download or upload.
* A value of 0 means unlimited.
* Default: 8

remote.s3.retry_policy = max_count
* Sets the retry policy to use for remote file operations.
* Optional.
* A retry policy specifies whether and how to retry file operations that fail
  for those failures that might be intermittent.
* Retry policies:
  + "max_count": Imposes a maximum number of times a file operation is
    retried upon intermittent failure both for individual parts of a multipart
    download or upload and for files as a whole.
* Default: max_count

remote.s3.max_count.max_retries_per_part = <unsigned integer>
* When the remote.s3.retry_policy setting is max_count, sets the maximum number
  of times a file operation is retried upon intermittent failure.
* Optional.
* The count is maintained separately for each file part in a multipart download
  or upload.
* Default: 9

remote.s3.max_count.max_retries_in_total = <unsigned integer>
* Optional.
* When the remote.s3.retry_policy setting is max_count, sets the maximum number
  of times a file operation is retried upon intermittent failure.
* The count is maintained for each file as a whole.
* Default: 128

remote.s3.timeout.connect = <unsigned integer>
* Optional
* Set the connection timeout, in milliseconds, to use when interacting with 
  S3 for this volume.
* Default: 5000 (5 seconds)

remote.s3.timeout.read = <unsigned integer>
* Optional
* Set the read timeout, in milliseconds, to use when interacting with S3 
  for this volume.
* Default: 60000 (60 seconds)

remote.s3.timeout.write = <unsigned integer>
* Optional
* Set the write timeout, in milliseconds, to use when interacting with S3 
  for this volume.
* Default: 60000 (60 seconds)

remote.s3.sslVerifyServerCert = <boolean>
* Optional.
* If this is set to true, Splunk verifies certificate presented by S3 
  server and checks that the common name/alternate name matches the 
  ones specified in 'remote.s3.sslCommonNameToCheck' 
  and 'remote.s3.sslAltNameToCheck'.
* Default: false

remote.s3.sslVersions = <versions_list>
* Optional.
* Comma-separated list of SSL versions to connect to 'remote.s3.endpoint'.
* The versions available are "ssl3", "tls1.0", "tls1.1", and "tls1.2".
* The special version "*" selects all supported versions.  The version "tls"
  selects all versions tls1.0 or newer.
* If a version is prefixed with "-" it is removed from the list.
* SSLv2 is always disabled; "-ssl2" is accepted in the version list but does nothing.
* When configured in FIPS mode, ssl3 is always disabled regardless
  of this configuration.
* Default: tls1.2

remote.s3.sslCommonNameToCheck = <commonName1>, <commonName2>, ..
* If this value is set, and 'remote.s3.sslVerifyServerCert' is set to 
  true, splunkd checks the common name of the certificate presented by
  the remote server (specified in 'remote.s3.endpoint') against this 
  list of common names.
* No default.

remote.s3.sslAltNameToCheck = <alternateName1>, <alternateName2>, ..
* If this value is set, and 'remote.s3.sslVerifyServerCert' is set to true,
  splunkd checks the alternate name(s) of the certificate presented by
  the remote server (specified in 'remote.s3.endpoint') against this list 
  of subject alternate names.
* No default.

remote.s3.sslRootCAPath = <path>
* Optional
* Full path to the Certificate Authority (CA) certificate PEM format file
  containing one or more certificates concatenated together. S3 certificate
  is validated against the CAs present in this file.
* Default: [sslConfig/caCertFile] in the server.conf file

remote.s3.cipherSuite = <cipher suite string>
* Optional.
* If set, uses the specified cipher string for the SSL connection.
* If not set, uses the default cipher string.
* Must specify 'dhFile' to enable any Diffie-Hellman ciphers.
* Default: TLSv1+HIGH:TLSv1.2+HIGH:@STRENGTH

remote.s3.ecdhCurves = <comma separated list of ec curves>
* Optional
* ECDH curves to use for ECDH key negotiation.
* The curves should be specified in the order of preference.
* The client sends these curves as a part of Client Hello.
* We only support named curves specified by their SHORT names.
  (see struct ASN1_OBJECT in asn1.h)
* The list of valid named curves by their short/long names can be obtained
  by executing this command:
  $SPLUNK_HOME/bin/splunk cmd openssl ecparam -list_curves
* e.g. ecdhCurves = prime256v1,secp384r1,secp521r1
* Default: not set

remote.s3.dhFile = <path>
* Optional
* PEM format Diffie-Hellman parameter file name.
* DH group size should be no less than 2048bits.
* This file is required in order to enable any Diffie-Hellman ciphers.
* Default: not set.

remote.s3.encryption = sse-s3 | sse-kms | sse-c | none
* Optional
* Specifies the scheme to use for Server-side Encryption (SSE) for 
  data-at-rest.
* sse-s3: Check http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
* sse-kms: Check http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
* sse-c: Check http://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html
* none: no Server-side encryption enabled. Data is stored unencrypted on 
  the remote storage.
* Default: none

remote.s3.encryption.sse-c.key_type = kms
* Optional
* Determines the mechanism Splunk uses to generate the key for sending 
  over to S3 for SSE-C.
* The only valid value is 'kms', indicating AWS KMS service.
* One must specify required KMS settings: e.g. remote.s3.kms.key_id
  for Splunk to start up while using SSE-C.
* Default: kms.

remote.s3.encryption.sse-c.key_refresh_interval = <unsigned integer>
* Optional
* Specifies the period, in seconds, at which a new key is generated and used
  for encrypting any new data being uploaded to S3.
* Default: 86400 (24 hours)

remote.s3.kms.key_id = <string>
* Required if remote.s3.encryption = sse-c | sse-kms
* Specifies the identifier for Customer Master Key (CMK) on KMS. It can be the
  unique key ID or the Amazon Resource Name (ARN) of the CMK or the alias
  name or ARN of an alias that refers to the CMK.
* Examples:
  Unique key ID: 1234abcd-12ab-34cd-56ef-1234567890ab
  CMK ARN: arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab
  Alias name: alias/ExampleAlias
  Alias ARN: arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias
* No default.

remote.s3.kms.access_key = <string>
* Optional.
* Similar to 'remote.s3.access_key'.
* If not specified, KMS access uses 'remote.s3.access_key'.
* No default.

remote.s3.kms.secret_key = <string>
* Optional.
* Similar to 'remote.s3.secret_key'.
* If not specified, KMS access uses 'remote.s3.secret_key'.
* No default.

remote.s3.kms.auth_region = <string>
* Required if 'remote.s3.auth_region' is not set and Splunk can not
  automatically extract this information.
* Similar to 'remote.s3.auth_region'.
* If not specified, KMS access uses 'remote.s3.auth_region'.
* No default.

remote.s3.kms.max_concurrent_requests = <unsigned integer>
* Optional.
* Limits maximum concurrent requests to KMS from this Splunk instance.
* NOTE: Can severely affect search performance if set to very low value.
* Default: 10

remote.s3.kms.<ssl_settings> = <...>
* Optional.
* Check the descriptions of the SSL settings for remote.s3.<ssl_settings>
  above. e.g. remote.s3.sslVerifyServerCert.
* Valid ssl_settings are sslVerifyServerCert, sslVersions, sslRootCAPath, sslAltNameToCheck,
  sslCommonNameToCheck, cipherSuite, ecdhCurves and dhFile.
* All of these are optional and fall back to same defaults as
  the 'remote.s3.<ssl_settings>'.