set -g default-terminal "screen-256color"



# remap prefix from 'C-b' to 'C-a'
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# split panes using | and -
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# reload config file (change file location to your the tmux.conf you want to use)
bind r source-file ~/.tmux.conf

# Enable mouse control (clickable windows, panes, resizable panes)
 set -g mouse on
# Enable mouse mode (tmux 2.1 and above)
##set -g mouse on



#    ██                              
#   ░██                              
#  ██████ ██████████  ██   ██ ██   ██
# ░░░██░ ░░██░░██░░██░██  ░██░░██ ██ 
#   ░██   ░██ ░██ ░██░██  ░██ ░░███  
#   ░██   ░██ ░██ ░██░██  ░██  ██░██ 
#   ░░██  ███ ░██ ░██░░██████ ██ ░░██
#    ░░  ░░░  ░░  ░░  ░░░░░░ ░░   ░░ 
# OPTIONS
set-option -g default-command /bin/zsh
set -g status on
set -g pane-base-index 1
set -g base-index 1
set -g set-titles on
set -g default-terminal "screen-256color"
set-option -g set-titles-string '#{pane_current_command}'
set-option -g history-limit 1024
#set-option -g visual-activity on
set-option -g status-position bottom
#set-option -g status-position top
set-option -g renumber-windows on
set-window-option -g monitor-activity off
set -g status-interval 1
set-option -g status-right-length 300

# SWITCHING
bind -n S-Left  previous-window
bind -n S-Right next-window

# RELOAD
bind r source-file ~/.tmux.conf

# MOUSE
#setw -g mode-mouse on
#set -g mouse-select-window on
#set -g mouse-select-pane on
#set -g mouse-resize-pane on

# SPLIT
set-option -g pane-active-border-fg colour0
set-option -g pane-active-border-bg default
set-option -g pane-border-fg colour0
set-option -g pane-border-bg default

# STATUS
set -g status-left ''
set -g status-right '#(python /home/julian/.tmux/status.py)'
set -g status-bg default
setw -g window-status-format '#[fg=colour1,bg=colour0] #W '
setw -g window-status-current-format '#[fg=colour0,bg=colour2] #W '




# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# Other examples:
# set -g @plugin 'github_username/plugin_name'
# set -g @plugin 'git@github.com/user/plugin'
# set -g @plugin 'git@bitbucket.com/user/plugin'


