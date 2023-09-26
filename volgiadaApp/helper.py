# Comparator for merge sort
def compare(team: dict, baseline: dict) -> int:
    if team['score'] < baseline['score']:
        return -1
    return 1

# Merge routine for merge sort
def merge(teams1: list[dict], teams2: list[dict]) -> list[dict]:
    mergedTeams = []; i = 0; j = 0

    while i < len(teams1) and j < len(teams2):
        if compare(teams1[i], teams2[j]) == -1:
            mergedTeams.append(teams1[i])
            i += 1; continue

        mergedTeams.append(teams2[j])
        j += 1

    # If some teams are still unassigned, append them
    if i != len(teams1):
        mergedTeams += teams1[i:]

    if j != len(teams2):
        mergedTeams += teams2[j:]

    return mergedTeams

# Merge sort to sort teams
def sortTeams(teams: list[dict]) -> list[dict]:
    if len(teams) <= 1:
        return teams
    
    half = len(teams) // 2
    return merge(sortTeams(teams[:half]), sortTeams(teams[half:]))