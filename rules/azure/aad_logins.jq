(:
  @Author: Antonio Blescia
  @Description: Detect AAD attempts outside ITALY. Manage also the IP Whitelisting for extra Italy IPs

  @Configuration:
    $white_list_ip: ip whitelist
    $files_path: csv log file/s path
:)

let $white_list_ip := ["46.101.70.71", (: VPN :) 
		    "51.83.165.95", (: OVH Lab :)
        		    "104.248.18.106" (: VPN Equixely :)
]

let $files_path := "./workbench/dataset/SignIns_2023-09-12_2023-10-12.csv"
for $event in csv-file($files_path,{"header": true})
where not ends-with($event.Location, "IT") and 
      not (some $val in $white_list_ip[] satisfies contains(upper-case($event."IP address"),upper-case($val)))
group by $username := $event.Username, $location := $event.Location
return { 

	"username" :$username, 
	"location": $location, 
	"ip_addresses": string-join(distinct-values($event."IP address"),", "), 
	"user_agents": string-join(distinct-values($event."User agent"),", ")
}