This module provides a 'NEMAC Mailing List' content type to facilitate
using Drupal to keep track of mailing list memberships.  Its purpose
is to facilitate synchronizing "groups" in a Google Apps account with
lists of email addresses stored in your Drupal site.  The module code
itself does not actually do any of this synchronization, or do
anything directly related to sending mail to lists.  It simply
facilitates using Drupal to keep track of lists of addresses.

Each 'NEMAC Mailing List' node instance consists of:

  (A) a "list address", which serves as the "title" of the node.  This
      should be the email address of a mailing list corresponding to a
      group in your Google Apps account
  (B) a collection of roles
  (C) a collection of user names
  (D) a collection of email addresses

The final list of addresses for the mailing list consists of the union
of the following:

  (1) email addresses of all users in any of the roles in (B) above
  (2) email addresses of all users in (C) above
  (3) the addresses in (D) above

This final list can be seen at any time by viewing a node's (full) page view.

The included drush script "getaddrs.php" may be run via drush at any
time to export the membership lists of all NEMAC Mailing List nodes on
the site.

CONFIGURATION AND USAGE

The module requires no configuration -- just enable it and start creating
nodes of type 'NEMAC Mailing List'.

The module comes with a python script called "sync_gapps_mailinglists"
that will synchronize the lists created in Drupal with actual groups
in a Google Apps account, and in order to function, this script
requires that you create a file called GAppsCredentials.py containin
the login creditials for your Google Apps account.  You can create
this file by making a copy of the file GAppsCredentials.tpl.py called
GAppsCredentials.py, and editing it to contain the relevant
credentials.  The account specified in that file must be one with
sufficient privledges in your Google Apps domain to create and manage
groups.

To use the "sync_gapps_mailinglists" script after you have created a
proper GAppsCredentials.py file, cd into this module directory, and
simply run the script with no arguments.  The current directory must
be this module directory.   This script does the following:

  (1) Use drush (which must be installed an on the shell's $PATH) to
      invoke the "getaddrs.php" script to get a list of all the mailing
      lists defined in your site, along with the list of member
      addresses for each list
  (2) Connects to the Google Apps server using the account specified in
      GAppsCredentials.py
  (3) For each mailing list found in (1):
      (3a) checks to see if a Google Group by that name exists, and if
           it does not, creates one
      (3b) adds any member email addresses found in (1) that are not
           present in the group, and deletes any addresses in the
           group that were not found in (1); the end result is that the
           Google Apps group membership will exactly match the
           list membership associated with the Drupal node for the
           list

Note the sync_gapps_mailinglists does not affect any groups present in
your Google Apps account that don't corespond to "NEMAC Mailing List"
nodes stored in the Drupal database.  So it's OK to have groups in
your Google Apps account that are not managed by this module, and the
module will not modify them.
