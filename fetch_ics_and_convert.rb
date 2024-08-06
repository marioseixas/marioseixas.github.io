require 'bundler/setup'
require 'net/http'
require 'uri'
require 'icalendar'
require 'json'
require 'yaml'
require 'digest'

config = YAML.load_file('_config.yml')
calendar_url = config['calendar']['url']
username = config['calendar']['username']
password = config['calendar']['password']

uri = URI(calendar_url)
req = Net::HTTP::Get.new(uri)
req.basic_auth(username, password)

res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == 'https') do |http|
  http.request(req)
end

if res.is_a?(Net::HTTPSuccess)
  calendar = Icalendar::Calendar.parse(res.body).first
  events = calendar.events.map do |event|
    {
      title: event.summary,
      start: event.dtstart.to_s,
      end: event.dtend.to_s
    }
  end

  File.write('_site/assets/data/events.json', JSON.pretty_generate(events))
else
  puts "Failed to fetch the calendar: #{res.message}"
end
