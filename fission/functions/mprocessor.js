module.exports = async function (context) {
  console.log(`Processed an mastodon data`);
  return {
    status: 200,
    body: JSON.stringify (context.request.body.map ((toot) => {
        return [{
          id: toot.id,
          created_at: toot.created_at,
          content: toot.content,
          account: toot.account,
        }];
      }
    ))
  };
}
