<?php

$result = db_select('node', 'n')
  ->fields('n', array('nid','title'))
  ->condition('type', 'nemac_mailing_list')
  ->execute();

while ($record = $result->fetchAssoc()) {
  $nid         = $record['nid'];
  $listaddress = $record['title'];
  $node        = node_load($nid);

  $addrs = nemac_mailing_list_addresses($node);

  printf("%s:%s\n", $listaddress, implode(",",$addrs));
}
