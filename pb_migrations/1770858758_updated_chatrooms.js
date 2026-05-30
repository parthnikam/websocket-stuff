/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3811774804")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE INDEX `idx_f0DrdtiH6K` ON `chatrooms` (`owner`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3811774804")

  // update collection data
  unmarshal({
    "indexes": []
  }, collection)

  return app.save(collection)
})
