Jekyll::Hooks.register :site, :post_write do |site|
    `npm exec -- pagefind --site ./github-pages-build/artifact --output-path pagefind`
end
