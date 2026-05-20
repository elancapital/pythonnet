using System.Collections.Generic;

using Python.Runtime;

namespace Python.Test
{
    public class IterableRegressionTester
    {
        public string PartialIterationDoesNotHoldGIL(IEnumerable<object> iterable)
        {
            var iterator = iterable.GetEnumerator();
            try
            {
                if (!iterator.MoveNext())
                {
                    return "empty";
                }

                if (DebugUtil.HaveInterpreterLock())
                {
                    return "gil_held_after_partial_iteration";
                }

                return "ok";
            }
            finally
            {
                iterator.Dispose();
            }
        }
    }
}
