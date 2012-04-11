<div id="nemac_mailing_list_addrs">
   <?php if ($addresses && count($addresses) > 0): ?>
   <b>Current member addresses:</b>
   <ul>
   <?php foreach ($addresses as $address): ?>
   <li><?php print $address; ?></li>
   <?php endforeach; ?>
   </ul>
   <?php else: ?>
   <b>There are no members currently on this mailing list.</b>
   <?php endif; ?>
</div>
