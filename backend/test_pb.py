from automation.playbooks import playbook_manager
print(f"Loaded {len(playbook_manager.get_all_playbooks())} playbooks")
for pb in playbook_manager.get_all_playbooks():
    print(pb.name)
