title: Linux System Administration
date: 2020-05-27
author: Harry
category: development

# Linux System Administration

## Process Management

### Investigating Processes

Certain shell variables hold process information.

`$$` contains the PID (process id) of the current process.

    echo $$

`$PPID` contains the PID of the **parent process** (the PPID), the process which spawned the current process.

    echo $PPID

Check the current PID, start a new bash process, and then verify that the PPID of that new bash process is the PID of the process from which the current process was spawned.

    echo $$;
    bash;
    echo $PPID;

Processes are created in 2 stages: fork, and exec. The spawning process first creates a copy of itself (the fork), then executes `exec` to replace the fork. `exec` can replace the current process with the command that it executes.

`ps` is a tool to examine processes. It can be invoked with various argument combinations. Two useful argument sets are `aux` and `fax`. 

`aux`, called as `ps aux`, contains `a`, `u`, and `x`, each of which controls some aspect of the output of `ps`. `a` shows processes from all users, `u` displays the owner of the process, and `x` shows 'headless' processes, those not attached to a terminal window. The `f` of `ps fax` stands for 'forest', is short for `--forest`, and shows the process with children in a tree-like view.

    ps fax;
    ps aux;

Using `ps` with `grep` is also effective:

    ps fax | grep mysql

`pgrep` can be used to search for a PID by process name, though it's utility is limited when there is more than one process with the same human readable name. For example:

    pgrep bash;

Very useful for an overview is `top`. `top` is a process manager which allows ordering by CPU%, by memory %, and so on. `top` can be invoked with arguments, or used interactively. Pressing `h` while in `top` will show help for interactive use. To invoke `top` with memory use ordering, for example:

    top -o %MEM


### Killing Processes

The primary way to stop a process is with `kill PID`. The `kill` command sends a signal to stop the process with PID.

    #kill 11025; # Don't run that unless you know what PID 11025 is!

There is a variety of signals which can be sent to processes with kill. The list can be viewed by typing `kill -l` at the terminal.

`kill -1` stands for the signal `SIGHUP`, which itself stands for 'signal hang up', a holdover from the days hardwire transmission. `kill -1 PID` forces the process specified by PID to re-read it's configuration file. This may have different effects with different programs specified by PID.

`kill -15` stands for `SIGTERM`, which stands for 'signal terminate'. `SIGTERM` is the standard signal sent with `kill`, when used without other arguments.

`kill -9` is `SIGKILL`. The difference between `SIGTERM` and `SIGKILL` is that `SIGKILL` is sent to the kernel, not the process, and it cannot be countermanded. `SIGKILL` is also called the 'sure kill'. The danger with `SIGKILL` is that it does not allow the killed process to perform any end of life cleanup, which can result in invalid state if used wantonly.

Processes can be suspended and resumed with `SIGSTOP` (`kill -19`) and `SIGCONT` (`kill -18`), respectively. Suspended processes remain in memory, but consume no CPU.

`pkill` is shorthand for finding a PID and issuing `kill PID` - it takes a process name. `pkill PID` is functionally equivalent to `kill $(pgrep process_name)`.

`killall` sends a `SIGTERM` to all processes with the supplied name:

    # killall mysql;

`killall` can be supplied with number arguments, just like `kill`, which change which signal is sent to the processes. A dangerous but sometimes necessary command is `killall -9 process_name`, which sends the `SIGKILL` signal to all processes named by process<sub>name</sub>.

Processes can be killed from inside the `top` manager, by pressing `k` inside the `top` view.


### Background Processes

Background jobs can be seen with the `jobs` commmand.

    jobs

`CTRL-Z` ****suspends a process, sending it to the background****, and halting it's operation. This is done by sending a `SIGSTOP` to the process. This could equally be accomplished with `kill -19` - `SIGSTOP`.

Starting a process with the `&` starts the process in the background, which can be quite handy:

    sudo service apache2 restart &

Using the `&`, we can restart Apache in the background, and if we dont redirect the standard out and error, they will be displayed on the terminal, without preventing further typing.

`jobs -p` will show the PIDs of the background jobs, as opposed to their command names.

The `fg` command brings a background job to the foreground - it can take a number, and bring that many jobs to the foreground:

    fg 3

The `bg` command ****restarts suspended background jobs****. It is a counterpart to `CTRL-Z`, as well as `fg`. `bg` can take a job number, which is usually given as `[NUM]+ Stopped [CMD NAME]` when viewing/backgrounding a process.

### Scheduling Jobs

#### One Time Jobs

Basic, one time scheduling can be achieved with `at`. Calling `at` will drop into a terminal based input, where one can define the command to be executed at the appointed time.

    at 09:00;

`atq` allows us to query jobs scheduled with `at`. `at -l` can also be used:

    atq;
    at -l;

`at` understands some English too, and if you don't specify the time, will assume you meant **the current time**, plus the qualifier:

    at next monday;
    atq;

`atrm` can remove jobs from the `at` queue.

    atrm 2;

Users can be permitted to use `at` by listing them in the file `/etc/at.allow`, and prevented by listing them in `/etc/at.deny`.



#### Repeated Jobs

`cron` is the well known command for scheduling jobs. Cron is incredibly useful, but as with all timing, it is important to get it right.

`crontab` is both a command, and the name of the configuration file. Every user can have their own `crontab`. The `crontab` format is five fields:

-   minute
-   hour
-   day of month
-   month
-   day of week

A `*` in any field means any value in that field.

One line in a `crontab` file looks like this:

    15 09 * 02 * python /path/to/script.py

Instead of scheduling using the five fields mentioned above, it is possible to schedule with some shorthand value:

-   `@reboot`
-   `@yearly`
-   `@annually`
-   `@monthly`
-   `@daily`
-   `@weekly`
-   `@hourly`
-   `@midnight`

The crontab file should not be edited directly - there is a dedicated edit mode which will use the text editor defined in the `EDITOR` or `VISUAL` environment variables. The edit mode is initiated with `crontab -e`, and the cron table can be viewed with `crontab -l`.

    crontab -l;
    crontab -e;

The crontab file is at `/etc/crontab`, and contains the `crontab` entries. The various period directories at `/etc/cron.*` contain the tasks to be executing with that periodicity, ie, `/etc/cron.daily`). There is one special directory, `/etc/cron.d`, for cases which need more control than the standard options.



## Login Logging

Various log files can be used to track logins:

-   `/var/log/wtmp`
-   `/var/log/btmp`
-   `/var/log/lastlog`
-   `/var/run/utmp`

The `who` command shows the currently logged in users, by reading the `/var/run/utmp` file:

    who

The `last` command shows a list of logins, read from the `/var/log/wtmp` file:

    last

The `last` command will also show reboots from that file, and one can specifically ask to see reboots:

    last reboot

The `lastlog` command reads from the `/var/log/lastlog` file, and shows the last login time of each user:

    lastlog | tail

The `lastb` command displays the contents of `/var/log/btmp`, which is updated on incorrect password attempts. ****This file does not log failed `ssh` attempts.****

    lastb;

If the file is not present, you can enable bad login logging by creating it.

    touch /var/log/btmp;

Failed superuser (`su`)and `ssh` login attempts will go to either `/var/log/secure`, or `/var/log/auth.log`, depending on the distribution. It is possible to create a custom log file, and direct failed superuser and `ssh` logins there:

    cd syslog_dir;
    echo "auth.*,authpriv.*    /path/to/custom.log" >> syslog.conf



# Syslog Daemon and `logger`

`syslogd` was the original system logger daemon. `rsyslogd` ('reliable `syslog`') is the backwards compatible, upgraded system logger. It uses `/etc/rsyslogd.conf`. There is some terminology necessary to understand `rsyslogd` configuration:

-   `facility`: where the message comes from
-   `priority`: how important/severe is the case
-   `action`: what to do with the message

Every line in the `.conf` file is an instruction on how to log something, using the terms listed above.

`rsyslog` has modules, which can be used to expand the functionality of the tool, for example, by logging to a database. `man rsyslog.conf`, and `man rsyslogd` contain plenty of information.

Facilities, as listed above, are the sources from which log messages can be drawn. These include:

-   `auth`
-   `authpriv`
-   `cron`
-   `daemon`
-   `ftp`
-   `kern`
-   `lpr mail`
-   `mark` (internal use)
-   `news`
-   `syslog`
-   `user`
-   `uucp`
-   `local0-7`

The difference between `auth` and `authpriv` is that `authpriv` denotes ****non-system authorization**** messages, whereas `auth` denotes authorization and authentication messages. `authpriv` can be configured with restricted permissions to log messages which may contain sensitive data.

You may notice `local0-7`. There are 8 facilities `0-7`, which are available to be configured for attached devices, or networked devices which support logging to syslog.

Log messages have priorities, here listed in ascending order:

-   `debug`
-   `info`
-   `notice`
-   `warning`
-   `err`
-   `crit`
-   `alert`
-   `emerg`

Choosing a severity level will automatically log any messages with a higher severity level. Adding `=`, will restrict the reported messages to exactly the severity specified (eg `=warning`). `.none` will prevent the facility to which it is applied from being reported.

The last component, actions, define what is done with the messages reported from facilities. The default action simply sends a message to the listed username. Any action ca be preceded with a `-` to prevent the log file from being synced after the message. The available actions are:

-   `root, myuser` -> comma separated list of users
-   `*`            -> all users
-   `/`            -> file (printer, console, tty, etc)
-   `-/`           -> file (but don't sync after writing)
-   `|`            -> named pipe
-   `@`            -> another syslog server hostname

An simple example configuration in `/etc/rsyslog.conf`:

    local0.emerg  /var/log/attached_device_emergency
    cron.=debug   myuser
    syslog.*      /var/log/all_syslog_messages

After changing the configuration, restart the service:

    sudo service rsyslog restart;

The `logger` command is useful for generating test messages for the logging configuration. It can also be used in scripts to actually log.

    logger -p local0.notice "some information";

`-p` is a flag to set the priority. More information can be found with `man logger`.

The way to watch logs in real time is with the `tail` command. `tail -f FILENAME` is similar to calling `tail FILENAME` each time a new log line is added to the file - it is a 'live updating' `tail`.

    tail -f /var/log/postgresql/postgresql-11-main.log;

Similarly, you can use the `watch` command. Preceding a command with `watch` will repeat the command, by default evey 2 seconds:

    watch whoami;

Log file sizes will eventually become cumbersome. It is common practice to 'rotate' log files, which means compressing and removing intermediate logs to keep the current log file manageable. The command for this is `logrotate`. The main `logrotate` configuration file is at `/etc/logrotate.conf`, and configuration for individual applications is at `/etc/logrotate.d/APPLICATION`.

## Resource Monitoring

### `top`

`top` is the standard way to monitor resources. `top` is an interactive monitoring tool which can show a variety of metrics. Among the ways `top` can be used are by pressing `k`, `t`, or `m`. `k` will cause `top` to request a PID to `kill`. `m` and `t` will toggle between displaying memory and task information. `top` can be called with arguments to customise its scope:

    top p 1 p 345;

The command above will restrict `top` to displaying information about processes with PIDs 1 and 345. More information can be found with `man top`.

Other tools for resource monitoring include `nmon` and `htop`. Both have a similar display to `top`, with more styling.


## Network Management

# Concepts

When talking about networking, it is necessary to have a model to contain the discussion. There are two commonly used models: the TCP/IP model and the Open Systems Integration (OSI) model.

## TCP/IP Model

The TCP/IP model has 4 layers:

-   Network Access Layer
-   Network Layer
-   Host-to-Host Layer
-   Application Layer

I prefer the more detailed OSI model, but the TCP/IP model roughly maps to the OSI model.   


## OSI Model

The OSI model has 7 layers:

-   Physical
-   Data Link
-   Network
-   Transport
-   Session
-   Presentation
-   Application


### Physical Layer (Layer 1)

The physical layer concerns things you might associate with electrical engineering: voltage, electrical signals, types of cable and connector, and so on. While this layer provides the foundation of the others, it is not specifically relevant to system administration.


### Data Link Layer (Layer 2)

This is the layer of bridges, switches, frames and MAC addresses - matters which sit **just above** the physical layer. Ethernet and Wireless device management occurs mostly at this layer, with protocols like the Address Resolution Protocol (`arp`) operating at this level. `ifconfig` (or the newer `ip` command) can give some information about the machine status with regard to the devices and protocols of this layer.


### Network Layer (Layer 3)

The network layer mainly concerns `ip` protocol packets. Hosts at this layer are identified by a 32 bit IP address. Other protocols operate on this layer, such as `icmp`. The `/etc/protocols` file has information on the protocols operative.


### Transport Layer (Layer 4)

The TCP/IP model calls this the 'host-to-host' layer. The protocols operative at this layer are `tcp` and `udp`.


### Session, Presentation, Application Layers (Layers 5, 6, 7)

These layers concern the handling of network data once it has left the Transport Layer, and so are more the concern of application security and networking.


## Casting

Along with the type of protocol (`DCHP`, `ARP`, `TCP/IP`, `BOOTP`, etc), the type of cast is an important feature of network communication. There are 4 types of cast:

-   Unicast: destined for exactly one recipient
-   Multicast: destined for a group of recipients
-   Broadcast: destined for every receiver on the network
-   Anycast: goes to the geographically nearest of a defined group.


## Network Interface Configuration

`/etc/network/interfaces` is a main network interface configuration file.

    cat /etc/network/interfaces;

The following configuration configures the `loopback` interface, and the `eth0` interface for DCHP (Dynamic Host Configuration Protocol):

    # The loopback network interface
    auto lo
    iface lo inet loopback
    auto eth0
    iface eth0 inet dhcp

The following configuration is how `/etc/network/interfaces` might look configured for a static ip address:

    auto eth0
    iface eth0 inet static
    address 10.42.189.198
    broadcast 10.42.189.207
    netmask 255.255.255.240
    gateway 10.42.189.193

`ifup` and `ifdown` are used to activate and deactivate network interfaces. Network interfaces **should** be deactivated before being reconfigured, but do not have to be.

`ifconfig` is the classic network interface configurator. Just typing `ifconfig` without arguments, will show the list of active network interfaces.

    ifconfig;

`ifconfig` can be supplied with the name of a network interface, which restricts the view to that interface:

    ifconfig eth0; # assuming your interface is called eth0...

`ifconfig` can activate and deactive the network interface. The difference from `ifup` and `ifdown` is that `ifconfig INTERFACE_NAME up/down` will deactivate/reactivate the interface **with the current configuration**, whereas `ifup/down` will reload the configuration from file, including any new configuration.

    ifconfig eth0 down;
    ifconfig eth0 up;
    ifconfig eth0;

`ifconfig` can set IP addresses and `MAC` addresses, which are retained until `ifdown/up` or reboot:

    ifconfig; # Check initial configuration
    ifconfig eth0 192.168.55.22 netmask 255.255.255.0.0; # Set the ip
    ifconfig eth0 hw ether 00:42:42:42:42:42; # Set the MAC
    ifconfig; # Check the changes
    ifdown && ifup; # Reset the changes
    ifconfig; # Check the reset

On some systems, the `ifconfig` command has been deprecated and replaced with the `ip` command, which is broadly similar, but has some different arguments and functionality:

    ip addr show; # Same as ifconfig
    ip addr show eth0; # Same as ifconfig eth0


`dhclient` is a daemon which manages the client side of the Dynamic Host Configuration Protocol (DHCP). DHCP enables a host to receive a local IP from a DHCP server. Typically your home router is a DCHP server for your local wifi network. If in use, `dhclient` will override any local ip configurations set with `ifconfig` or `ip` when it receives a new ip from teh DHCP server.

Every host (machine) is given a `hostname`, and often positioned in a DNS namespace, to give a fully qualified domain name, for example, 'blog.this.com'. On Debian and Debian-derived distros, the hostname can be found (and set) in `/etc/hostname`.

The `hostname` can be temporarily set using `hostname NEW_HOSTNAME`:

    cat /etc/hostname; # Read hostname from file
    hostname some-new-hostname; # Temporarily set a new hostname
    hostname; # Check the new hostname

`sysctl` can be used to read and write the `hostname`:

    sysctl kernel.hostname; # What is the current hostname?
    sysctl kernel.hostname = another-hostname; # Set a different hostname
    sysctl kernel.hostname; # Check using sysctl
    hostname; # Check using hostname command

The `arp` command can be used to manipulate the system ARP cache - the list of machines recently communicated with. ARP is the Address Resolution Protocol, a Data Link (2) Layer protocol, which enables IP addresses to be resolved to MAC (Media Access Control) addresses. IP addresses identify a host on the Network (3) Layer, MAC addresses identify a machine on the Data Link (2) Layer. 

List the hosts in the ARP cache with:

    arp; # Standard
    arp -a; # Alternative 'BSD style' no columns view

Remove an ARP cache entry with:

    arp -d IP_OR_HOSTNAME; # Requires root

The `route` command will show the machine's local routing table, as will `netstat -r`. `route` also allows one to manipulate the routing table:

    route add default gw SOME_IP; # Add a default gateway 

`man route` will give more information about the other features of `route`.

`ping` is an extremely useful tool for checking connection status. `ping` sends Internet Control Message Protocol (ICMP) packets to the target IP, and reports back any errors, packet loss, network latency, etc. It is almost certainly the fastest way to check whether a machine is connected to a network.

    ping 192.168.0.1;


## `ssh`

`ssh` is the Secure Shell. `ssh` uses public-key cryptography to authenticate with a remote host and provide a secure and private connection with that host.

`/etc/ssh/` is where much of the `ssh` configuration is to be found. Each user also has a `.ssh/` directory, in which a file named `config` can be placed to define the connection configuration for specified remote hosts.

A `~/.ssh/config` file might look like this:

    Host host1
        HostName SOME.IP.HERE
        User some-user
        Port 22 # usually
        IdentityFile path/to/ssh/key/here
    
    Host host2
        HostName ANOTHER.IP.HERE
        User a-different-user
        Port specify-a-different-port

