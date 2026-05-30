/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_493096279")

  // remove field
  collection.fields.removeById("date1330254257")

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_493096279")

  // add field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "date1330254257",
    "max": "",
    "min": "",
    "name": "date_time",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "date"
  }))

  return app.save(collection)
})
