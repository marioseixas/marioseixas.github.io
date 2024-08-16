Jekyll::Hooks.register :site, :post_write do |site|
  system("npx -y pagefind --site '%{path}'" % {:path => site.dest})
end
