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
-   `yearly`
-   `annually`
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