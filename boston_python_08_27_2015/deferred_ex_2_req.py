from requests import get

req = get('https://api.github.com/users/clokep/orgs')

print("Organization request done!")
# Parse the JSON payload. TODO Error checking.
orgs = req.json()
# The names of the organizations in alphabetical order.
org_names = sorted([bytes(org['login']) for org in orgs])

# Now request the repos under each org.
org_list = []
for org in org_names:
    print("\t%s" % org)  # print out the org
    req = get('https://api.github.com/orgs/%s/repos' % org)

    print("Got repo information for %s" % org)

    # Parse the JSON payload. TODO Error checking.
    repos = req.json()
    if not repos:  # no repos, return early
        continue
    # The names of the repos in alphabetical order.
    names = sorted([repo['name'] for repo in repos])
    org_list.append((org, names))

print("Outputting repos")
for org, repos in org_list:
    print('\t%s: %s' % (org, ', '.join(repos) if repos else '(none)'))
