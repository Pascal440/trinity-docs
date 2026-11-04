"""Receive a single workbook on stdin and return its recalculated PDF on stdout."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException


def option(name, value):
    item = PropertyValue()
    item.Name = name
    item.Value = value
    return item


with tempfile.TemporaryDirectory(dir="/tmp") as directory:
    workspace = Path(directory)
    workbook = workspace / "workbook.xlsx"
    pdf = workspace / "preview.pdf"
    data = sys.stdin.buffer.read(25 * 1024**2 + 1)
    if not data.startswith(b"PK") or len(data) > 25 * 1024**2:
        raise SystemExit("Classeur XLSX invalide ou trop volumineux.")
    workbook.write_bytes(data)
    endpoint = f"pipe,name=demo01a_{os.getpid()};urp;StarOffice.ComponentContext"
    office = subprocess.Popen(
        ["libreoffice", "--headless", "--norestore",
         f"-env:UserInstallation={uno.systemPathToFileUrl(str(workspace / 'profile'))}",
         f"--accept={endpoint}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    document = None
    try:
        resolver = uno.getComponentContext().ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", uno.getComponentContext()
        )
        for _ in range(100):
            try:
                context = resolver.resolve(f"uno:{endpoint}")
                break
            except NoConnectException:
                time.sleep(0.1)
        else:
            raise RuntimeError("LibreOffice indisponible.")
        desktop = context.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context
        )
        document = desktop.loadComponentFromURL(
            uno.systemPathToFileUrl(str(workbook)), "_blank", 0,
            (option("Hidden", True), option("ReadOnly", True),
             option("MacroExecutionMode", 0), option("UpdateDocMode", 0)),
        )
        if not document or not document.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
            raise RuntimeError("Document tableur non reconnu.")
        document.calculateAll()
        document.storeToURL(
            uno.systemPathToFileUrl(str(pdf)),
            (option("FilterName", "calc_pdf_Export"),
             option("FilterData", uno.Any("[]com.sun.star.beans.PropertyValue",
                                         (option("SinglePageSheets", True),)))),
        )
        sys.stdout.buffer.write(pdf.read_bytes())
    finally:
        try:
            if document:
                document.close(True)
        finally:
            office.terminate()
            try:
                office.wait(timeout=5)
            except subprocess.TimeoutExpired:
                office.kill()
                office.wait()
