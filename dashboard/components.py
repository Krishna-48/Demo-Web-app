
def styled_status(status):
    if status=='Recovered':
        return '✅ Recovered'
    if status=='In Progress':
        return '🔶 In Progress'
    if status=='Failed':
        return '❌ Failed'
    return status or 'Unknown'
