title: Linux System Administration
date: 2020-05-27
author: Harry
category: development

# Linux System Administration

## Chapter 1: Process Management

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


