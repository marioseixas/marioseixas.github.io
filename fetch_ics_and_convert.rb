require 'net/http'
require 'uri'
require 'icalendar'
require 'json'
require 'digest/md5'

url = "https://dav.heydola.com/dav.php/calendars/py28wj81/default/?export"
username = "py28wj81"
password = "20287290"

uri = URI(url)
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Get.new(uri.request_uri)
request.basic_auth(username, password)

response = http.request(request)

if response.code.to_i == 200
  puts "Access successful!"
  calendar = Icalendar::Calendar.parse(response.body).first

  events = calendar.events.map do |event|
    {
      "title" => event.summary,
      "start" => event.dtstart.to_time.iso8601,
      "end" => event.dtend.to_time.iso8601
    }
  end

  File.open("events.json", "w") do |f|
    f.write(JSON.pretty_generate(events))
  end
else
  puts "Failed to access. Status code: #{response.code}"
  puts response.body
end
