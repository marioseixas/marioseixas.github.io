Jekyll::Hooks.register :site, :post_write do |site|
    `npx -y pagefind --site ./_site --output-path ./_site/pagefind`
end
