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
