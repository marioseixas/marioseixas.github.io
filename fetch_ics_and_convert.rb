require 'bundler/setup'
require 'net/http'
require 'uri'
require 'icalendar'
require 'json'
require 'yaml'
require 'digest'

uri = URI('https://dav.heydola.com/dav.php/calendars/py28wj81/default/?export')

# Create HTTP object and request
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
request = Net::HTTP::Get.new(uri.request_uri)
request.basic_auth('py28wj81', '20287290')

# Fetch the calendar data
response = http.request(request)

if response.code == '200'
  cals = Icalendar::Calendar.parse(response.body)
  events = cals.flat_map(&:events).map do |event|
    {
      id: Digest::MD5.hexdigest(event.uid),
      title: event.summary,
      start: event.dtstart.to_s,
      end: event.dtend.to_s,
      location: event.location,
      description: event.description
    }
  end

  # Save events to JSON file
  File.open('_site/assets/data/events.json', 'w') do |file|
    file.write(JSON.pretty_generate(events))
  end
else
  puts "Failed to fetch the calendar: #{response.message}"
end
