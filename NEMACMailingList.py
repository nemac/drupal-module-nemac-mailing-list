import re
import subprocess
import gdata.apps.service
import gdata.apps.groups.service

DRYRUN = False

def array_to_dict(array):
  d = {}
  for a in array:
    d[a] = 1
  return d

class MailingListManger:
  def __init__(self):
    self.initialized = True

class GappsMailingListManager(MailingListManger):

  def __init__(self, user, domain, password):
    self.user = user
    self.domain = domain
    self.password = password
    self.groupsService = gdata.apps.groups.service.GroupsService(email=self.user, domain=self.domain, password=self.password)
    self.groupsService.ProgrammaticLogin()
    self.managed_group_description = 'Group managed by nemac_mailing_list Drupal module; do not edit manually.'

  def list_address(self, list):
    if re.search(r'@[^@]+.[^@]+', list):
      return list
    else:
      return list + "@" + self.domain

  def list_name(self, listaddress):
    return 'DRUPAL-' + re.sub(r'@.*$', '', listaddress)

  def get_lists(self):
    groups = self.groupsService.RetrieveAllGroups()
    return sorted([group['groupId'] for group in groups])

  def get_list_members(self,listname):
    members = self.groupsService.RetrieveAllMembers(listname)
    return sorted([x['memberId'] for x in members])

  def add_member_to_list(self,member,group):
    print "    +  %s" % (member)
    if not DRYRUN:
      self.groupsService.AddMemberToGroup(member, group)

  def remove_member_from_list(self,member,group):
    print "    -  %s" % (member)
    if not DRYRUN:
      self.groupsService.RemoveMemberFromGroup(member, group)

  def list_exists(self, list):
    return self.list_address(list) in self.get_lists()

  def create_list(self, list):
    if not self.list_exists(list):
      print 'create list: ' + list
      if not DRYRUN:
        self.groupsService.CreateGroup(list, self.list_name(list), self.managed_group_description, 'Anyone')

  def update_list_description(self, list):
    if not DRYRUN:
      self.groupsService.UpdateGroup(list, self.list_name(list), self.managed_group_description, 'Anyone')

  def sync_list(self, group, new_members):
    print "%s:" % group
    if not self.list_exists(group):
      self.create_list(group)
    else:
      self.update_list_description(group)
    existing_members = self.get_list_members(group)
    existing_member_dict = array_to_dict(existing_members)
    new_member_dict      = array_to_dict(new_members)
    for m in new_members:
      if not m in existing_member_dict:
        self.add_member_to_list(m, group)
    for m in existing_members:
      if not m in new_member_dict:
        self.remove_member_from_list(m, group)


class DrupalMailingListManager(MailingListManger):

  def get_mcrn_mailinglists_from_drupal(self):
    #output = subprocess.check_output(["/usr/local/bin/drush", "scr", "getaddrs.php"])
    output = subprocess.Popen(["/usr/local/bin/drush", "scr", "getaddrs.php"], stdout=subprocess.PIPE).communicate()[0]
    mailinglists = {}
    for line in output.split('\n'):
      match = re.search(r'^([a-zA-Z0-9_-]+@[a-zA-Z0-9_\.-]+):(.*)$', line)
      if match:
        listaddress   = re.sub(r'@.*$', '', match.group(1)) # remove the '@nemac.org' from the end of the address
        listaddresses = match.group(2).split(',')
        mailinglists[listaddress] = listaddresses
    return mailinglists

  def __init__(self):
    self.mailinglists = self.get_mcrn_mailinglists_from_drupal()

  def get_lists(self):
    return sorted([name for name in self.mailinglists])

  def get_list_members(self,listname):
    return sorted(self.mailinglists[listname])
