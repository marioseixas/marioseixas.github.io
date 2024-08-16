Jekyll::Hooks.register :site, :post_write do |site|
  system("npx -y pagefind --source '%{path}'" % {:path => site.dest})
end
